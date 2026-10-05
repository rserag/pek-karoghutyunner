#!/usr/bin/env python3
"""Calculate verified quarterly receipts; no extraction, rates, or legal decisions."""
import argparse
import calendar
import html
import json
import os
import re
import sys
import tempfile
from datetime import date
from decimal import Context, Decimal, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext
from pathlib import Path
from urllib.parse import urlparse


ROUNDING = {'truncate': ROUND_DOWN, 'half_up': ROUND_HALF_UP, 'half_even': ROUND_HALF_EVEN}
RATE_RULES = {'before_receipt', 'same_day', 'on_or_before_receipt'}
FX_FIELDS = {'rate_date', 'rate_amd', 'rate_unit', 'rate_source', 'verified_on'}


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


def day(value, label):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'{label} must use YYYY-MM-DD')
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f'{label} is not a valid date') from error


def decimal(value, label, allow_zero=False):
    # Floats and booleans are deliberately rejected: the JSON must preserve decimals.
    if type(value) is int:
        value = str(value)
    if not isinstance(value, str) or len(value) > 100 or not re.fullmatch(r'\d+(?:\.\d+)?', value):
        raise ValueError(f'{label} must be an unsigned decimal string or integer')
    number = Decimal(value)
    if len(number.as_tuple().digits) > 28 or not number.is_finite():
        raise ValueError(f'{label} must contain at most 28 decimal digits')
    if number < 0 or (number == 0 and not allow_zero):
        raise ValueError(f'{label} must be {"nonnegative" if allow_zero else "positive"}')
    return number


def mode(mapping, key, allowed):
    value = required(mapping, key)
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f'rounding.{key} must be one of: {", ".join(sorted(allowed))}')
    return value


def plain(number):
    return format(number, 'f')


def calculate(data):
    """Return deterministic arithmetic for externally verified inputs.

    No working-day calendar, law, rate source, or income eligibility is verified here.
    Quarter membership and FX comparisons use receipt_date only. A legally verified
    basis using another recognition date requires a separate reviewed calculation.
    Precise conversions use 256-digit Decimal precision before the selected rounding.
    """
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    year = integer(required(data, 'year'), 'year', 1, 9999)
    quarter = integer(required(data, 'quarter'), 'quarter', 1, 4)
    basis = string(required(data, 'basis'), 'basis')
    if required(data, 'method_verified') is not True:
        raise ValueError('method_verified must be true after external method verification')
    rule = required(data, 'rate_date_rule')
    if not isinstance(rule, str) or rule not in RATE_RULES:
        raise ValueError('rate_date_rule must be before_receipt, same_day, or on_or_before_receipt')
    rounding = required(data, 'rounding')
    if not isinstance(rounding, dict):
        raise ValueError('rounding must be an object')
    receipt_mode = mode(rounding, 'per_receipt', {'half_up', 'half_even'})
    declaration_mode = mode(rounding, 'declaration', set(ROUNDING))
    tax_rate = None
    if 'tax_rate' in data:
        tax_rate = decimal(data['tax_rate'], 'tax_rate', allow_zero=True)
        if tax_rate > 1:
            raise ValueError('tax_rate must be a fraction between 0 and 1')
        tax_mode = mode(rounding, 'tax', set(ROUNDING))
    elif 'tax' in rounding:
        raise ValueError('rounding.tax requires tax_rate')
    if set(rounding) - {'per_receipt', 'declaration', 'tax'}:
        raise ValueError('Unknown rounding policy field')
    payments = required(data, 'payments')
    if not isinstance(payments, list):
        raise ValueError('payments must be a list')
    if not payments and data.get('zero_receipts_confirmed') is not True:
        raise ValueError('Empty payments require zero_receipts_confirmed: true')
    month = 3 * quarter - 2
    start = date(year, month, 1)
    end = date(year, month + 2, calendar.monthrange(year, month + 2)[1])
    rows, seen, totals = [], set(), {}
    precise_total, rounded_total = Decimal(0), Decimal(0)
    # A new Context also isolates traps and exponent limits, not just rounding.
    with localcontext(Context(prec=256, rounding=ROUND_HALF_EVEN)):
        for payment in payments:
            if not isinstance(payment, dict):
                raise ValueError('Each payment must be an object')
            ref = string(required(payment, 'transaction_ref'), 'transaction_ref')
            if ref in seen:
                raise ValueError('Duplicate transaction_ref; reconcile repeated statement rows')
            seen.add(ref)
            receipt = day(required(payment, 'receipt_date'), 'receipt_date')
            if not start <= receipt <= end:
                raise ValueError('Receipt outside requested quarter')
            currency = required(payment, 'currency')
            if not isinstance(currency, str) or not re.fullmatch(r'[A-Z]{3}', currency):
                raise ValueError('currency must be an uppercase three-letter code')
            amount = decimal(required(payment, 'amount'), 'amount')
            if 'source_page' in payment:
                integer(payment['source_page'], 'source_page', 1, 1000000)
            for label in ('payer', 'memo'):
                if label in payment and not isinstance(payment[label], str):
                    raise ValueError(f'{label} must be a string')
            row = dict(payment, transaction_ref=ref, amount=plain(amount))
            if currency == 'AMD':
                if FX_FIELDS.intersection(payment):
                    raise ValueError('AMD receipts use the amount directly; omit FX fields')
                precise = amount
            else:
                rate_day = day(required(payment, 'rate_date'), 'rate_date')
                verified = day(required(payment, 'verified_on'), 'verified_on')
                if verified < rate_day:
                    raise ValueError('verified_on cannot precede rate_date')
                valid_day = {'before_receipt': rate_day < receipt,
                             'same_day': rate_day == receipt,
                             'on_or_before_receipt': rate_day <= receipt}[rule]
                if not valid_day:
                    raise ValueError('rate_date does not satisfy the selected rate_date_rule')
                rate = decimal(required(payment, 'rate_amd'), 'rate_amd')
                unit = decimal(required(payment, 'rate_unit'), 'rate_unit')
                source = string(required(payment, 'rate_source'), 'rate_source')
                parsed = urlparse(source)
                if parsed.scheme not in ('https', 'http') or not parsed.netloc:
                    raise ValueError('rate_source must be an absolute HTTP(S) URL')
                precise = amount * rate / unit
                row.update(rate_amd=plain(rate), rate_unit=plain(unit), rate_source=source)
            rounded = precise.quantize(Decimal('0.01'), rounding=ROUNDING[receipt_mode])
            row.update(precise_amd=plain(precise), rounded_amd=plain(rounded))
            rows.append(row)
            totals[currency] = totals.get(currency, Decimal(0)) + amount
            precise_total += precise
            rounded_total += rounded
        whole = rounded_total.to_integral_value(rounding=ROUNDING[declaration_mode])
        result = dict(data, year=year, quarter=quarter, basis=basis, payments=rows,
                      quarter_start=str(start), quarter_end=str(end),
                      currency_totals={key: plain(value) for key, value in sorted(totals.items())},
                      precise_total_amd=plain(precise_total),
                      rounded_total_amd=plain(rounded_total),
                      whole_dram_income=plain(whole),
                      calculation_precision=256)
        if tax_rate is not None:
            result['tax_rate'] = plain(tax_rate)
            result['estimated_whole_dram_tax'] = plain(
                (whole * tax_rate).to_integral_value(rounding=ROUNDING[tax_mode]))
    return result


def render(data):
    """Render a report without injecting source text or assuming tax rules."""
    esc = lambda value: html.escape(str(value), quote=True)
    rows = []
    for row in data['payments']:
        conversion = 'Native AMD; no FX conversion' if row['currency'] == 'AMD' else (
            f"{row['rate_amd']} AMD per {row['rate_unit']} {row['currency']}; "
            f"published {row['rate_date']}; verified {row['verified_on']}")
        source = row.get('rate_source', '')
        parsed = urlparse(source)
        source_cell = (f'<a href="{esc(source)}" rel="noopener noreferrer">{esc(source)}</a>'
                       if parsed.scheme in ('https', 'http') and parsed.netloc else esc(source or 'Not applicable'))
        evidence_cell = '<br>'.join(f'{label}: {esc(row[key])}' for key, label in
                                   (('payer', 'Payer'), ('memo', 'Memo'), ('source_page', 'Statement page'))
                                   if key in row) or 'Not supplied'
        cells = (row['transaction_ref'], row['receipt_date'], row['currency'], row['amount'], conversion)
        rows.append('<tr>' + ''.join(f'<td>{esc(value)}</td>' for value in cells)
                    + f'<td>{source_cell}</td><td>{evidence_cell}</td>'
                    + f'<td>{esc(row["precise_amd"])}</td><td>{esc(row["rounded_amd"])}</td></tr>')
    tax = ''
    if 'estimated_whole_dram_tax' in data:
        with localcontext(Context(prec=256, rounding=ROUND_HALF_EVEN)):
            percent = plain(Decimal(data['tax_rate']) * 100)
        tax = f"<p>Estimated tax at {esc(percent)}%: {esc(data['estimated_whole_dram_tax'])} AMD.</p>"
    currencies = ', '.join(f'{value} {code}' for code, value in data['currency_totals'].items()) or 'None'
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<title>Q{data['quarter']} {data['year']} income calculation</title>
<style>body{{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 20px;color:#173042}}table{{border-collapse:collapse;width:100%;margin:24px 0}}th,td{{padding:10px;border-bottom:1px solid #d6e1e7;text-align:left;overflow-wrap:anywhere}}.total{{background:#edf5f8;padding:20px;border-radius:10px}}</style>
<h1>Q{data['quarter']} {data['year']} income calculation</h1>
<p>{esc(data['quarter_start'])} – {esc(data['quarter_end'])}</p>
<p>Recognition basis: {esc(data['basis'])}. Verified FX date rule: {esc(data['rate_date_rule'])}.</p>
<p>Rounding: {esc(json.dumps(data['rounding'], sort_keys=True))}. Native-currency totals: {esc(currencies)}.</p>
<table><thead><tr><th>Transaction</th><th>Received</th><th>Currency</th><th>Amount</th><th>Conversion</th><th>Rate source</th><th>Statement evidence</th><th>Before receipt rounding (AMD)</th><th>Rounded receipt (AMD)</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<div class="total"><p>Total before receipt rounding: {esc(data['precise_total_amd'])} AMD.</p>
<p>Sum of rounded receipts: {esc(data['rounded_total_amd'])} AMD.</p>
<p>Whole-dram declaration input: {esc(data['whole_dram_income'])} AMD.</p>{tax}</div>
<p>The caller verified the method and source evidence. Quarter membership and FX comparisons use receipt_date only; a verified basis requiring another recognition date needs a separate reviewed calculation. This calculator does not retrieve rates, verify working-day calendars, determine taxable receipts, establish legal eligibility, or submit a declaration. Unrounded division uses {data['calculation_precision']}-digit Decimal precision; repeating quotients remain approximations.</p></html>'''


def write_private(path, content):
    """Write UTF-8 atomically with user-only permissions on POSIX systems."""
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.income-', dir=path.parent)
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
        result = calculate(data)
        report = render(result) if args.html else None
        write_private(args.output, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        if args.html:
            write_private(args.html, report)
    except (ValueError, OSError, UnicodeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    print(f"Rounded income AMD {result['rounded_total_amd']}; whole dram {result['whole_dram_income']}; "
          f"estimated tax {result.get('estimated_whole_dram_tax', 'not requested')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
