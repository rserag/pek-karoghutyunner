"""Synthetic annual-evidence tests; no taxpayer, statement or live portal data."""
import copy
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from decimal import Inexact, Rounded, ROUND_DOWN, ROUND_UP, localcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills' / 'armenia-tax-income' / 'scripts' / 'reconcile_annual.py'
SPEC = importlib.util.spec_from_file_location('annual_reconciliation', SCRIPT)
annual = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(annual)


def sample():
    return json.loads((ROOT / 'examples' / 'annual.synthetic.json').read_text(encoding='utf-8'))


class AnnualReconciliationTests(unittest.TestCase):
    def test_complete_fixture_retains_rounding_and_excludes_old_versions(self):
        result = annual.reconcile(sample())
        self.assertTrue(result['complete'])
        self.assertTrue(result['annual_audit_complete'])
        self.assertTrue(result['filing_review_complete'])
        self.assertEqual(result['annual_precise_total_amd'], '6001.259')
        self.assertEqual(result['annual_rounded_receipts_total_amd'], '6001.25')
        self.assertEqual(result['annual_accepted_whole_dram_turnover'], '6001')
        self.assertEqual(result['accepted_turnover_minus_precise_audit_amd'], '-0.259')
        self.assertEqual(result['verified_no_return_quarters'], [3])
        self.assertEqual(result['missing_record_quarters'], [])
        corrected = result['quarters'][1]
        self.assertEqual(corrected['current_filing_ref'], 'SYNTHETIC-Q2-CORRECTION-2')
        self.assertEqual(corrected['accepted_whole_dram_turnover'], '2001')
        self.assertEqual(len(corrected['filings']), 3)

    def test_missing_quarter_is_unknown_and_never_a_zero(self):
        data = sample()
        data['quarters'] = data['quarters'][:3]
        result = annual.reconcile(data)
        self.assertFalse(result['complete'])
        self.assertEqual(result['missing_record_quarters'], [4])
        self.assertEqual(result['missing_audit_quarters'], [4])
        self.assertEqual(result['unknown_filing_quarters'], [4])
        self.assertIsNone(result['annual_precise_total_amd'])
        self.assertIsNone(result['annual_accepted_whole_dram_turnover'])
        self.assertIsNone(result['accepted_turnover_minus_precise_audit_amd'])
        self.assertEqual(result['known_precise_total_amd'], '3001.005')
        self.assertEqual(result['known_accepted_whole_dram_turnover'], '3001')
        self.assertIsNone(result['quarters'][3]['audit'])

    def test_empty_quarters_does_not_establish_no_income(self):
        data = sample()
        data['quarters'] = []
        result = annual.reconcile(data)
        self.assertEqual(result['missing_record_quarters'], [1, 2, 3, 4])
        self.assertEqual(result['known_precise_total_amd'], '0')
        self.assertIsNone(result['annual_precise_total_amd'])
        self.assertIsNone(result['annual_accepted_whole_dram_turnover'])

    def test_known_audit_and_unknown_filing_are_independent(self):
        data = sample()
        row = data['quarters'][3]
        row.update(state='unknown', unknown_reason='SYNTHETIC archive status not yet established')
        del row['filings']
        result = annual.reconcile(data)
        self.assertTrue(result['annual_audit_complete'])
        self.assertFalse(result['filing_review_complete'])
        self.assertEqual(result['annual_precise_total_amd'], '6001.259')
        self.assertIsNone(result['annual_accepted_whole_dram_turnover'])
        self.assertEqual(result['unknown_filing_quarters'], [4])

    def test_accepted_return_with_unknown_audit_is_independent(self):
        data = sample()
        del data['quarters'][0]['audit']
        result = annual.reconcile(data)
        self.assertTrue(result['filing_review_complete'])
        self.assertFalse(result['annual_audit_complete'])
        self.assertEqual(result['annual_accepted_whole_dram_turnover'], '6001')
        self.assertIsNone(result['annual_precise_total_amd'])
        self.assertEqual(result['missing_audit_quarters'], [1])

    def test_no_return_does_not_imply_zero_audited_income(self):
        data = sample()
        del data['quarters'][2]['audit']
        result = annual.reconcile(data)
        self.assertTrue(result['filing_review_complete'])
        self.assertFalse(result['annual_audit_complete'])
        self.assertIsNone(result['annual_precise_total_amd'])
        self.assertEqual(result['missing_audit_quarters'], [3])
        # Legal applicability is externally reviewed; this helper cannot infer zero.
        data = sample()
        audit = data['quarters'][2]['audit']
        audit.update(precise_total_amd='12.345', rounded_total_amd='12.35')
        del audit['zero_income_evidence']
        result = annual.reconcile(data)
        self.assertEqual(result['annual_precise_total_amd'], '6013.604')
        self.assertEqual(result['annual_accepted_whole_dram_turnover'], '6001')

    def test_zero_audit_requires_explicit_evidence(self):
        data = sample()
        del data['quarters'][2]['audit']['zero_income_evidence']
        with self.assertRaisesRegex(ValueError, 'zero_income_evidence'):
            annual.reconcile(data)
        data = sample()
        data['quarters'][2]['audit']['rounded_total_amd'] = '1'
        with self.assertRaisesRegex(ValueError, 'zero precise audit'):
            annual.reconcile(data)
        data = sample()
        data['quarters'][0]['audit']['zero_income_evidence'] = 'SYNTHETIC conflicting zero'
        with self.assertRaisesRegex(ValueError, 'zero precise audit'):
            annual.reconcile(data)

    def test_supplied_audit_requires_verified_method_and_evidence(self):
        for field in ('basis', 'source_evidence', 'precise_total_amd', 'rounded_total_amd'):
            with self.subTest(field=field):
                data = sample()
                del data['quarters'][0]['audit'][field]
                with self.assertRaises(ValueError):
                    annual.reconcile(data)
        for value in (False, 1, 'true', None):
            with self.subTest(value=value):
                data = sample()
                data['quarters'][0]['audit']['method_verified'] = value
                with self.assertRaisesRegex(ValueError, 'method_verified'):
                    annual.reconcile(data)

    def test_duplicate_record_identity_or_quarter_is_rejected(self):
        data = sample()
        data['quarters'][1]['record_id'] = ' ' + data['quarters'][0]['record_id'] + ' '
        with self.assertRaisesRegex(ValueError, 'Duplicate record_id'):
            annual.reconcile(data)
        data = sample()
        data['quarters'][1]['quarter'] = 1
        with self.assertRaisesRegex(ValueError, 'Duplicate taxpayer/year/quarter'):
            annual.reconcile(data)

    def test_year_and_taxpayer_must_match(self):
        for field, value in (('year', 2024), ('taxpayer_tin', 'SYNTHETIC-OTHER-TAXPAYER')):
            with self.subTest(field=field):
                data = sample()
                data['quarters'][0][field] = value
                with self.assertRaisesRegex(ValueError, 'must match'):
                    annual.reconcile(data)

    def test_filing_references_unique_across_the_full_year(self):
        data = sample()
        data['quarters'][3]['filings'][0]['filing_ref'] = (
            ' ' + data['quarters'][0]['filings'][0]['filing_ref'])
        with self.assertRaisesRegex(ValueError, 'Duplicate filing_ref'):
            annual.reconcile(data)

    def test_current_version_cannot_be_guessed(self):
        data = sample()
        filings = data['quarters'][1]['filings']
        filings[0]['state'] = 'current_accepted'
        del filings[0]['superseded_by_filing_ref']
        filings[0]['current_version_evidence'] = 'SYNTHETIC competing current claim'
        with self.assertRaisesRegex(ValueError, 'exactly one current'):
            annual.reconcile(data)
        data = sample()
        del data['quarters'][1]['filings'][-1]['current_version_evidence']
        with self.assertRaisesRegex(ValueError, 'current_version_evidence'):
            annual.reconcile(data)
        data = sample()
        filings = data['quarters'][1]['filings']
        filings[-1].update(state='superseded_accepted',
                           superseded_by_filing_ref='SYNTHETIC-UNSUPPLIED-CORRECTION')
        del filings[-1]['current_version_evidence']
        with self.assertRaisesRegex(ValueError, 'exactly one current'):
            annual.reconcile(data)

    def test_correction_links_must_be_complete_acyclic_and_same_form(self):
        data = sample()
        data['quarters'][1]['filings'][0]['superseded_by_filing_ref'] = 'SYNTHETIC-MISSING'
        with self.assertRaisesRegex(ValueError, 'reference a filing in this quarter'):
            annual.reconcile(data)
        data = sample()
        filings = data['quarters'][1]['filings']
        filings[1]['superseded_by_filing_ref'] = filings[0]['filing_ref']
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            annual.reconcile(data)
        data = sample()
        data['quarters'][1]['filings'][0]['form_number'] = 240
        with self.assertRaisesRegex(ValueError, 'same form_number'):
            annual.reconcile(data)

    def test_conflicting_states_are_rejected(self):
        for mutation in ('no_return_on_accepted', 'filing_on_no_return',
                         'unknown_on_no_return', 'no_return_on_unknown'):
            with self.subTest(mutation=mutation):
                data = sample()
                if mutation == 'no_return_on_accepted':
                    data['quarters'][0]['no_return_reason'] = 'SYNTHETIC conflicting status'
                elif mutation == 'filing_on_no_return':
                    data['quarters'][2]['filings'] = []
                elif mutation == 'unknown_on_no_return':
                    data['quarters'][2]['unknown_reason'] = 'SYNTHETIC conflicting status'
                else:
                    row = data['quarters'][2]
                    row.update(state='unknown', unknown_reason='SYNTHETIC unresolved')
                with self.assertRaises(ValueError):
                    annual.reconcile(data)

    def test_no_return_requires_reason_and_evidence(self):
        for field in ('no_return_reason', 'no_return_evidence'):
            with self.subTest(field=field):
                data = sample()
                del data['quarters'][2][field]
                with self.assertRaisesRegex(ValueError, field):
                    annual.reconcile(data)

    def test_numbers_reject_floats_negative_values_and_false_precision(self):
        for field in ('precise_total_amd', 'rounded_total_amd'):
            for value in (100.1, True, '-1', -1, '1e3', '1,000', 'NaN', 'Infinity',
                          '1.0 ', None, '1' * 29):
                with self.subTest(field=field, value=value):
                    data = sample()
                    data['quarters'][0]['audit'][field] = value
                    with self.assertRaises(ValueError):
                        annual.reconcile(data)
        for value in ('1000.0', 1000.0, True, '-1', '-0', '1e3'):
            with self.subTest(filed=value):
                data = sample()
                data['quarters'][0]['filings'][0]['whole_dram_turnover'] = value
                with self.assertRaises(ValueError):
                    annual.reconcile(data)

    def test_year_quarter_and_form_require_actual_integers(self):
        for field, value in (('year', True), ('year', '2025'), ('quarter', 1.0),
                             ('quarter', 0), ('quarter', 5)):
            with self.subTest(field=field, value=value):
                data = sample()
                data['quarters'][0][field] = value
                with self.assertRaises(ValueError):
                    annual.reconcile(data)
        data = sample()
        data['quarters'][0]['filings'][0]['form_number'] = '286'
        with self.assertRaises(ValueError):
            annual.reconcile(data)

    def test_unknown_fields_cannot_hide_a_misspelled_status_or_amount(self):
        for place in ('input', 'quarter', 'audit', 'filing'):
            with self.subTest(place=place):
                data = sample()
                target = {'input': data, 'quarter': data['quarters'][0],
                          'audit': data['quarters'][0]['audit'],
                          'filing': data['quarters'][0]['filings'][0]}[place]
                target['misspelled_input'] = 'SYNTHETIC'
                with self.assertRaisesRegex(ValueError, 'unknown fields'):
                    annual.reconcile(data)

    def test_decimal_precision_and_caller_context_do_not_change_totals(self):
        expected = annual.reconcile(sample())
        for rounding in (ROUND_UP, ROUND_DOWN):
            with self.subTest(rounding=rounding), localcontext() as context:
                context.prec = 4
                context.Emax = 5
                context.Emin = -5
                context.rounding = rounding
                context.traps[Inexact] = True
                context.traps[Rounded] = True
                self.assertEqual(annual.reconcile(sample()), expected)
        data = sample()
        for row in data['quarters']:
            audit = row['audit']
            audit.update(precise_total_amd='9' * 28, rounded_total_amd='9' * 28)
            audit.pop('zero_income_evidence', None)
        self.assertEqual(annual.reconcile(data)['annual_precise_total_amd'],
                         str(4 * int('9' * 28)))

    def test_input_order_does_not_select_versions_or_quarters(self):
        data = sample()
        data['quarters'].reverse()
        data['quarters'][2]['filings'].reverse()
        result = annual.reconcile(data)
        self.assertEqual([row['quarter'] for row in result['quarters']], [1, 2, 3, 4])
        self.assertEqual(result['annual_accepted_whole_dram_turnover'], '6001')
        self.assertEqual(result['quarters'][1]['current_filing_ref'],
                         'SYNTHETIC-Q2-CORRECTION-2')

    def test_html_escapes_evidence_and_displays_incomplete_totals(self):
        data = sample()
        data['basis'] = '<script>alert("basis")</script>'
        data['quarters'][0]['source_evidence'] = '<img src=x onerror=alert(1)>'
        data['quarters'][0]['filings'][0]['acceptance_evidence'] = 'javascript:alert(1)'
        del data['quarters'][0]['audit']
        report = annual.render(annual.reconcile(data))
        self.assertIn('Incomplete supplied evidence', report)
        self.assertIn('Unknown AMD', report)
        self.assertIn('&lt;script&gt;', report)
        self.assertIn('&lt;img ', report)
        self.assertNotIn('<script>', report)
        self.assertNotIn('<img ', report)
        self.assertNotIn('href=', report)
        self.assertIn('Superseded by SYNTHETIC-Q2-CORRECTION-2', report)

    def test_input_is_not_mutated(self):
        data = sample()
        before = copy.deepcopy(data)
        annual.reconcile(data)
        self.assertEqual(data, before)


class AnnualCliTests(unittest.TestCase):
    def run_cli(self, source, target, report=None):
        args = [sys.executable, str(SCRIPT), str(source), '--output', str(target)]
        if report is not None:
            args.extend(['--html', str(report)])
        return subprocess.run(args, text=True, capture_output=True)

    def test_private_atomic_outputs_and_unicode_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / 'input.json'
            target = folder / 'private' / 'result.json'
            report = folder / 'private' / 'report.html'
            data = sample()
            data['basis'] = 'SYNTHETIC Սինթետիկ օրինակ'
            source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            result = self.run_cli(source, target, report)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(target.read_text(encoding='utf-8'))['basis'], data['basis'])
            self.assertIn(data['basis'], report.read_text(encoding='utf-8'))
            self.assertEqual(list(target.parent.glob('.annual-*')), [])
            if os.name == 'posix':
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(report.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(target.parent.stat().st_mode), 0o700)

    def test_partial_evidence_produces_an_explicit_incomplete_result(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'input.json', Path(directory) / 'result.json'
            data = sample()
            data['quarters'] = []
            source.write_text(json.dumps(data), encoding='utf-8')
            result = self.run_cli(source, target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('incomplete', result.stdout)
            self.assertFalse(json.loads(target.read_text(encoding='utf-8'))['complete'])

    def test_validation_error_does_not_write_or_expose_identifiers(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'input.json', Path(directory) / 'result.json'
            data = sample()
            data['quarters'][0]['taxpayer_tin'] = 'SYNTHETIC-MISMATCH-MUST-NOT-BE-PRINTED'
            source.write_text(json.dumps(data), encoding='utf-8')
            result = self.run_cli(source, target)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())
            self.assertNotIn('SYNTHETIC-MISMATCH-MUST-NOT-BE-PRINTED', result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_path_collisions_never_overwrite_input_or_json(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'input.json', Path(directory) / 'result.json'
            original = json.dumps(sample())
            source.write_text(original, encoding='utf-8')
            result = self.run_cli(source, source)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_text(encoding='utf-8'), original)
            result = self.run_cli(source, target, target)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())

    def test_json_nonfinite_numbers_are_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / 'input.json', Path(directory) / 'result.json'
            source.write_text('{"year": NaN}', encoding='utf-8')
            result = self.run_cli(source, target)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(target.exists())
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
