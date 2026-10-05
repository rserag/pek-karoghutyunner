#!/usr/bin/env python3
"""Reconcile verified quarterly evidence; no tax, eligibility or filing decisions."""
import argparse
import html
import json
import os
import re
import sys
import tempfile
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from pathlib import Path


QUARTER_STATES = {'accepted', 'verified_no_return', 'unknown'}
FILING_STATES = {'current_accepted', 'superseded_accepted'}


def required(mapping, key):
    if key not in mapping:
        raise ValueError(f'Missing required field: {key}')
    return mapping[key]


def string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string')
    return value.strip()


def integer(value, label, lower, upper):
    if type(value) is not int or not lower <= value <= upper:
        raise ValueError(f'{label} must be an integer from {lower} to {upper}')
    return value


def money(value, label, whole=False):
    if type(value) is int:
        value = str(value)
    pattern = r'\d+' if whole else r'\d+(?:\.\d+)?'
    if not isinstance(value, str) or len(value) > 100 or not re.fullmatch(pattern, value):
        unit = 'whole-dram' if whole else 'decimal'
        raise ValueError(f'{label} must be an unsigned {unit} string or integer')
    amount = Decimal(value)
    if not amount.is_finite() or len(amount.as_tuple().digits) > 28:
        raise ValueError(f'{label} must contain at most 28 decimal digits')
    return amount


def plain(amount):
    return format(amount, 'f')


def known_fields(mapping, allowed, label):
    extra = set(mapping) - set(allowed)
    if extra:
        raise ValueError(f'{label}: unknown fields: {", ".join(sorted(extra))}')


def audit_record(value):
    if not isinstance(value, dict):
        raise ValueError('audit must be an object')
    known_fields(value, {'method_verified', 'basis', 'source_evidence',
                         'precise_total_amd', 'rounded_total_amd',
                         'zero_income_evidence'}, 'audit')
    if required(value, 'method_verified') is not True:
        raise ValueError('audit.method_verified must be true after external verification')
    basis = string(required(value, 'basis'), 'audit.basis')
    evidence = string(required(value, 'source_evidence'), 'audit.source_evidence')
    precise = money(required(value, 'precise_total_amd'), 'audit.precise_total_amd')
    rounded = money(required(value, 'rounded_total_amd'), 'audit.rounded_total_amd')
    # A known zero needs affirmative source review, never a missing statement.
    zero_evidence = None
    if precise == 0:
        zero_evidence = string(required(value, 'zero_income_evidence'),
                               'audit.zero_income_evidence')
        if rounded != 0:
            raise ValueError('A zero precise audit cannot have nonzero rounded income')
    elif 'zero_income_evidence' in value:
        raise ValueError('zero_income_evidence requires a zero precise audit')
    result = dict(method_verified=True, basis=basis, source_evidence=evidence,
                  precise_total_amd=plain(precise), rounded_total_amd=plain(rounded))
    if zero_evidence is not None:
        result['zero_income_evidence'] = zero_evidence
    return result


def filing_records(values, seen_refs):
    if not isinstance(values, list) or not values:
        raise ValueError('An accepted quarter requires a nonempty filings list')
    filings, by_ref, current = [], {}, []
    for value in values:
        if not isinstance(value, dict):
            raise ValueError('Each filing must be an object')
        known_fields(value, {'filing_ref', 'form_number', 'state',
                             'whole_dram_turnover', 'acceptance_evidence',
                             'current_version_evidence', 'superseded_by_filing_ref'}, 'filing')
        ref = string(required(value, 'filing_ref'), 'filing_ref')
        if ref in seen_refs:
            raise ValueError('Duplicate filing_ref; reconcile duplicate report evidence')
        seen_refs.add(ref)
        form = integer(required(value, 'form_number'), 'form_number', 1, 999999)
        state = required(value, 'state')
        if not isinstance(state, str) or state not in FILING_STATES:
            raise ValueError('filing.state must be current_accepted or superseded_accepted')
        turnover = money(required(value, 'whole_dram_turnover'),
                         'whole_dram_turnover', whole=True)
        evidence = string(required(value, 'acceptance_evidence'), 'acceptance_evidence')
        filing = dict(filing_ref=ref, form_number=form, state=state,
                      whole_dram_turnover=plain(turnover), acceptance_evidence=evidence)
        if state == 'current_accepted':
            if 'superseded_by_filing_ref' in value:
                raise ValueError('A current filing cannot also be superseded')
            filing['current_version_evidence'] = string(
                required(value, 'current_version_evidence'), 'current_version_evidence')
            current.append(filing)
        else:
            if 'current_version_evidence' in value:
                raise ValueError('A superseded filing cannot claim to be current')
            filing['superseded_by_filing_ref'] = string(
                required(value, 'superseded_by_filing_ref'), 'superseded_by_filing_ref')
        filings.append(filing)
        by_ref[ref] = filing
    if len(current) != 1:
        raise ValueError('Each accepted quarter requires exactly one current accepted filing')
    if len({filing['form_number'] for filing in filings}) != 1:
        raise ValueError('Correction versions must have the same form_number')
    # Follow externally supplied correction links; do not choose by filing date.
    current_ref = current[0]['filing_ref']
    for filing in filings:
        ref, path = filing['filing_ref'], set()
        while ref != current_ref:
            if ref in path:
                raise ValueError('Cyclic superseded filing links')
            path.add(ref)
            target = by_ref.get(ref)
            if target is None:
                raise ValueError('Superseded filing link must reference a filing in this quarter')
            ref = target.get('superseded_by_filing_ref')
            if ref is None:
                raise ValueError('Superseded filing links must lead to the current filing')
    return filings, current[0]


def reconcile(data):
    """Sum supplied verified evidence without interpreting tax law or calendars.

    Missing quarters and missing audits remain unknown. A documented no-return
    state completes filing review only; it never establishes zero audited income.
    """
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    known_fields(data, {'year', 'taxpayer_tin', 'basis', 'quarters'}, 'input')
    year = integer(required(data, 'year'), 'year', 1, 9999)
    tin = string(required(data, 'taxpayer_tin'), 'taxpayer_tin')
    basis = string(required(data, 'basis'), 'basis')
    values = required(data, 'quarters')
    if not isinstance(values, list):
        raise ValueError('quarters must be a list')
    by_quarter, seen_ids, seen_refs = {}, set(), set()
    for value in values:
        if not isinstance(value, dict):
            raise ValueError('Each quarterly record must be an object')
        known_fields(value, {'record_id', 'year', 'taxpayer_tin', 'quarter', 'state',
                             'source_evidence', 'audit', 'filings', 'no_return_reason',
                             'no_return_evidence', 'unknown_reason'}, 'quarter')
        record_id = string(required(value, 'record_id'), 'record_id')
        if record_id in seen_ids:
            raise ValueError('Duplicate record_id; reconcile duplicate quarterly evidence')
        seen_ids.add(record_id)
        record_year = integer(required(value, 'year'), 'quarter.year', 1, 9999)
        record_tin = string(required(value, 'taxpayer_tin'), 'quarter.taxpayer_tin')
        if record_year != year or record_tin != tin:
            raise ValueError('Quarterly record year and taxpayer_tin must match the annual request')
        quarter = integer(required(value, 'quarter'), 'quarter', 1, 4)
        if quarter in by_quarter:
            raise ValueError('Duplicate taxpayer/year/quarter; combine versions in one filings list')
        state = required(value, 'state')
        if not isinstance(state, str) or state not in QUARTER_STATES:
            raise ValueError('quarter.state must be accepted, verified_no_return, or unknown')
        evidence = string(required(value, 'source_evidence'), 'quarter.source_evidence')
        row = dict(record_id=record_id, quarter=quarter, state=state,
                   source_evidence=evidence, audit=None, filings=[],
                   current_filing_ref=None, accepted_whole_dram_turnover=None,
                   accepted_turnover_minus_precise_audit_amd=None)
        if 'audit' in value:
            row['audit'] = audit_record(value['audit'])
        if state == 'accepted':
            if {'no_return_reason', 'no_return_evidence', 'unknown_reason'}.intersection(value):
                raise ValueError('An accepted quarter cannot also claim no return or unknown status')
            filings, current = filing_records(required(value, 'filings'), seen_refs)
            row.update(filings=filings, current_filing_ref=current['filing_ref'],
                       accepted_whole_dram_turnover=current['whole_dram_turnover'])
        else:
            if 'filings' in value:
                raise ValueError('Only accepted quarterly records may contain filings')
            if state == 'verified_no_return':
                if 'unknown_reason' in value:
                    raise ValueError('A verified no-return quarter cannot also be unknown')
                row['no_return_reason'] = string(required(value, 'no_return_reason'),
                                                 'no_return_reason')
                row['no_return_evidence'] = string(required(value, 'no_return_evidence'),
                                                   'no_return_evidence')
            else:
                if {'no_return_reason', 'no_return_evidence'}.intersection(value):
                    raise ValueError('An unknown quarter cannot claim verified no-return evidence')
                row['unknown_reason'] = string(required(value, 'unknown_reason'), 'unknown_reason')
        by_quarter[quarter] = row
    missing_records = [quarter for quarter in range(1, 5) if quarter not in by_quarter]
    rows = []
    precise_total, rounded_total, accepted_total = Decimal(0), Decimal(0), Decimal(0)
    # Isolate caller precision, traps and exponent limits, as in the quarterly helper.
    with localcontext(Context(prec=256, rounding=ROUND_HALF_EVEN)):
        for quarter in range(1, 5):
            row = by_quarter.get(quarter)
            if row is None:
                row = dict(record_id=None, quarter=quarter, state='unknown',
                           source_evidence=None, audit=None, filings=[], current_filing_ref=None,
                           accepted_whole_dram_turnover=None,
                           accepted_turnover_minus_precise_audit_amd=None,
                           unknown_reason='No quarterly evidence supplied')
            audit = row['audit']
            if audit is not None:
                precise_total += Decimal(audit['precise_total_amd'])
                rounded_total += Decimal(audit['rounded_total_amd'])
            filed = row['accepted_whole_dram_turnover']
            if filed is not None:
                accepted_total += Decimal(filed)
                if audit is not None:
                    row['accepted_turnover_minus_precise_audit_amd'] = plain(
                        Decimal(filed) - Decimal(audit['precise_total_amd']))
            rows.append(row)
        missing_audits = [row['quarter'] for row in rows if row['audit'] is None]
        unknown_filings = [row['quarter'] for row in rows if row['state'] == 'unknown']
        audit_complete, filing_complete = not missing_audits, not unknown_filings
        difference = (plain(accepted_total - precise_total)
                      if audit_complete and filing_complete else None)
    return dict(year=year, taxpayer_tin=tin, basis=basis, quarters=rows,
                annual_audit_complete=audit_complete, filing_review_complete=filing_complete,
                complete=audit_complete and filing_complete,
                missing_record_quarters=missing_records, missing_audit_quarters=missing_audits,
                unknown_filing_quarters=unknown_filings,
                verified_no_return_quarters=[row['quarter'] for row in rows
                                             if row['state'] == 'verified_no_return'],
                known_precise_total_amd=plain(precise_total),
                known_rounded_receipts_total_amd=plain(rounded_total),
                known_accepted_whole_dram_turnover=plain(accepted_total),
                annual_precise_total_amd=plain(precise_total) if audit_complete else None,
                annual_rounded_receipts_total_amd=plain(rounded_total) if audit_complete else None,
                annual_accepted_whole_dram_turnover=plain(accepted_total) if filing_complete else None,
                accepted_turnover_minus_precise_audit_amd=difference,
                calculation_precision=256)


def render(data):
    """Render private evidence as escaped text, without source-supplied links."""
    esc = lambda value: html.escape(str(value), quote=True)
    amount = lambda value: 'Unknown' if value is None else esc(value)
    rows = []
    for row in data['quarters']:
        audit = row['audit'] or {}
        details = [row.get('source_evidence'), row.get('no_return_reason'),
                   row.get('no_return_evidence'), row.get('unknown_reason'),
                   audit.get('basis'), audit.get('source_evidence'), audit.get('zero_income_evidence')]
        for filing in row['filings']:
            details.append(f"{filing['filing_ref']}: {filing['state']}; form {filing['form_number']}; "
                           f"turnover {filing['whole_dram_turnover']} AMD")
            details.append(filing['acceptance_evidence'])
            details.append(filing.get('current_version_evidence'))
            if 'superseded_by_filing_ref' in filing:
                details.append('Superseded by ' + filing['superseded_by_filing_ref'])
        cells = (f"Q{row['quarter']}", row['state'], row['current_filing_ref'] or 'None')
        rows.append('<tr>' + ''.join(f'<td>{esc(value)}</td>' for value in cells)
                    + f'<td>{amount(audit.get("precise_total_amd"))}</td>'
                    + f'<td>{amount(audit.get("rounded_total_amd"))}</td>'
                    + f'<td>{amount(row["accepted_whole_dram_turnover"])}</td>'
                    + f'<td>{amount(row["accepted_turnover_minus_precise_audit_amd"])}</td>'
                    + '<td>' + '<br>'.join(esc(value) for value in details if value) + '</td></tr>')
    status = 'Complete supplied evidence' if data['complete'] else 'Incomplete supplied evidence'
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<title>{esc(data['year'])} annual income reconciliation</title>
<style>body{{font:16px system-ui;max-width:1200px;margin:40px auto;padding:0 20px;color:#173042}}table{{border-collapse:collapse;width:100%;margin:24px 0}}th,td{{padding:10px;border-bottom:1px solid #d6e1e7;text-align:left;vertical-align:top;overflow-wrap:anywhere}}.total{{background:#edf5f8;padding:20px;border-radius:10px}}</style>
<h1>{esc(data['year'])} annual income reconciliation</h1>
<p>Taxpayer reference: {esc(data['taxpayer_tin'])}. {esc(data['basis'])}.</p>
<p>{esc(status)}. Missing quarterly records: {esc(data['missing_record_quarters'])}; missing audits: {esc(data['missing_audit_quarters'])}; unknown filing states: {esc(data['unknown_filing_quarters'])}.</p>
<table><thead><tr><th>Quarter</th><th>Review state</th><th>Current filing</th><th>Precise audit (AMD)</th><th>Rounded receipts (AMD)</th><th>Current filed turnover (AMD)</th><th>Filed minus precise audit (AMD)</th><th>Evidence and correction history</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<div class="total"><p>Verified annual precise audit: {amount(data['annual_precise_total_amd'])} AMD.</p>
<p>Verified annual sum of rounded receipts: {amount(data['annual_rounded_receipts_total_amd'])} AMD.</p>
<p>Reviewed annual sum of current accepted whole-dram turnover: {amount(data['annual_accepted_whole_dram_turnover'])} AMD.</p>
<p>Filed minus precise audit: {amount(data['accepted_turnover_minus_precise_audit_amd'])} AMD.</p>
<p>Known subtotals only: precise audit {esc(data['known_precise_total_amd'])}; rounded receipts {esc(data['known_rounded_receipts_total_amd'])}; current accepted turnover {esc(data['known_accepted_whole_dram_turnover'])} AMD.</p></div>
<p>Differences need explanation; the totals are retained separately without changing or rounding either one. A verified no-return state does not establish zero income. Superseded returns remain evidence and are excluded from the accepted-turnover sum. Completeness reflects supplied evidence only.</p>
<p>This helper does not verify law, eligibility, income recognition, actual source authenticity, suspension calendars or filing requirements. It does not calculate social contributions, tax, payments or annual form inputs, and does not operate the portal.</p></html>'''


def write_private(path, content):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.annual-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            output.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--html', type=Path)
    args = parser.parse_args(argv)
    try:
        paths = [args.input.resolve(), args.output.resolve()]
        if args.html:
            paths.append(args.html.resolve())
        if len(set(paths)) != len(paths):
            raise ValueError('Input, JSON output, and HTML output must be different paths')
        def invalid_constant(_value):
            raise ValueError('JSON NaN and infinity are not supported')
        data = json.loads(args.input.read_text(encoding='utf-8'), parse_constant=invalid_constant)
        result = reconcile(data)
        report = render(result) if args.html else None
        write_private(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        if args.html:
            write_private(args.html, report)
    except (ValueError, OSError, UnicodeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    print(f"Annual audit {'complete' if result['annual_audit_complete'] else 'incomplete'}; "
          f"filing review {'complete' if result['filing_review_complete'] else 'incomplete'}; "
          f"known precise audit {result['known_precise_total_amd']} AMD; "
          f"known accepted turnover {result['known_accepted_whole_dram_turnover']} AMD")
    return 0


if __name__ == '__main__':
    sys.exit(main())
