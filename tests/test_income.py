"""Synthetic regression tests; no real taxpayer or financial data."""
import copy
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, Inexact, Rounded, ROUND_DOWN, ROUND_UP, localcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills' / 'armenia-tax-income' / 'scripts' / 'calculate.py'
SPEC = importlib.util.spec_from_file_location('income_calculator', SCRIPT)
calculator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calculator)


def sample():
    return json.loads((ROOT / 'examples' / 'income.synthetic.json').read_text(encoding='utf-8'))


def single(amount='100', rate='400', unit='1'):
    data = sample()
    data.pop('tax_rate')
    data['rounding'].pop('tax')
    row = data['payments'][0]
    row.update(amount=amount, rate_amd=rate, rate_unit=unit)
    data['payments'] = [row]
    return data


class IncomeCalculationTests(unittest.TestCase):
    def test_synthetic_mixed_currency_fixture(self):
        result = calculator.calculate(sample())
        self.assertEqual(Decimal(result['precise_total_amd']), Decimal('77345.67'))
        self.assertEqual(result['rounded_total_amd'], '77345.67')
        self.assertEqual(result['whole_dram_income'], '77345')
        self.assertEqual(result['estimated_whole_dram_tax'], '1546')
        self.assertEqual(result['currency_totals'], {'AMD': '12345.67', 'JPY': '10000', 'USD': '100.00'})

    def test_leap_year_and_quarter_boundaries(self):
        data = single()
        for receipt in ('2024-01-01', '2024-02-29', '2024-03-31'):
            with self.subTest(receipt=receipt):
                data['payments'][0].update(receipt_date=receipt, rate_date='2023-12-29')
                result = calculator.calculate(data)
                self.assertEqual(result['quarter_start'], '2024-01-01')
                self.assertEqual(result['quarter_end'], '2024-03-31')
        for receipt in ('2023-12-31', '2024-04-01'):
            with self.subTest(receipt=receipt):
                data['payments'][0]['receipt_date'] = receipt
                with self.assertRaisesRegex(ValueError, 'outside requested quarter'):
                    calculator.calculate(data)

    def test_year_and_quarter_require_integers(self):
        for field, values in (('year', ['2024', 2024.0, True, 0, 10000]),
                              ('quarter', ['1', 1.1, True, 0, 5])):
            for value in values:
                with self.subTest(field=field, value=value):
                    data = single()
                    data[field] = value
                    with self.assertRaises(ValueError):
                        calculator.calculate(data)

    def test_amd_receipts_need_no_fx(self):
        data = single()
        data['payments'] = [{'transaction_ref': 'SYN-NATIVE', 'receipt_date': '2024-03-31',
                             'currency': 'AMD', 'amount': '12345.67'}]
        result = calculator.calculate(data)
        self.assertEqual(result['precise_total_amd'], '12345.67')
        self.assertIn('Native AMD; no FX conversion', calculator.render(result))

    def test_amd_receipts_reject_conflicting_fx(self):
        data = single()
        data['payments'][0]['currency'] = 'AMD'
        with self.assertRaisesRegex(ValueError, 'omit FX fields'):
            calculator.calculate(data)

    def test_quote_unit_is_used_and_reported(self):
        data = single('10000', '250', '100')
        data['payments'][0]['currency'] = 'JPY'
        result = calculator.calculate(data)
        self.assertEqual(result['precise_total_amd'], '25000')
        self.assertIn('250 AMD per 100 JPY', calculator.render(result))

    def test_duplicate_identity_rejected_across_pages(self):
        data = single()
        data['payments'].append(dict(data['payments'][0], source_page=2, memo='Repeated page'))
        with self.assertRaisesRegex(ValueError, 'Duplicate transaction_ref'):
            calculator.calculate(data)

    def test_duplicate_identity_normalizes_surrounding_whitespace(self):
        data = single()
        data['payments'].append(dict(data['payments'][0], transaction_ref=' ' + data['payments'][0]['transaction_ref']))
        with self.assertRaisesRegex(ValueError, 'Duplicate transaction_ref'):
            calculator.calculate(data)

    def test_distinct_identical_amounts_are_retained(self):
        data = single()
        data['payments'].append(dict(data['payments'][0], transaction_ref='SYN-DISTINCT'))
        self.assertEqual(calculator.calculate(data)['rounded_total_amd'], '80000.00')

    def test_method_must_be_explicitly_verified(self):
        for value in (False, 1, 'true', None):
            with self.subTest(value=value):
                data = single()
                data['method_verified'] = value
                with self.assertRaisesRegex(ValueError, 'method_verified'):
                    calculator.calculate(data)

    def test_rate_date_policies(self):
        cases = [('before_receipt', '2024-02-28', True),
                 ('before_receipt', '2024-02-29', False),
                 ('same_day', '2024-02-29', True),
                 ('same_day', '2024-02-28', False),
                 ('on_or_before_receipt', '2024-02-28', True),
                 ('on_or_before_receipt', '2024-02-29', True),
                 ('on_or_before_receipt', '2024-03-01', False)]
        for rule, rate_day, valid in cases:
            with self.subTest(rule=rule, rate_day=rate_day):
                data = single()
                data['rate_date_rule'] = rule
                data['payments'][0]['rate_date'] = rate_day
                if valid:
                    calculator.calculate(data)
                else:
                    with self.assertRaisesRegex(ValueError, 'rate_date_rule'):
                        calculator.calculate(data)

    def test_invalid_dates_are_rejected(self):
        for field in ('receipt_date', 'rate_date', 'verified_on'):
            for value in ('2024-02-30', '20240229', '2024-2-29', ''):
                with self.subTest(field=field, value=value):
                    data = single()
                    data['payments'][0][field] = value
                    with self.assertRaises(ValueError):
                        calculator.calculate(data)

    def test_verification_cannot_predate_publication(self):
        data = single()
        data['payments'][0]['verified_on'] = '2024-02-27'
        with self.assertRaisesRegex(ValueError, 'verified_on cannot precede'):
            calculator.calculate(data)

    def test_monetary_values_reject_inexact_or_invalid_inputs(self):
        for field in ('amount', 'rate_amd', 'rate_unit'):
            for value in (100.1, True, 'NaN', 'Infinity', '1e3', '-1', '0', '1,000',
                          '1.0 ', None, '1' * 29):
                with self.subTest(field=field, value=value):
                    data = single()
                    data['payments'][0][field] = value
                    with self.assertRaises(ValueError):
                        calculator.calculate(data)

    def test_exact_json_integers_are_accepted_for_money(self):
        result = calculator.calculate(single(100, 400, 1))
        self.assertEqual(result['precise_total_amd'], '40000')

    def test_currency_format_validation(self):
        for value in ('usd', '', 'US', 'NOT-A-CURRENCY', 1):
            with self.subTest(value=value):
                data = single()
                data['payments'][0]['currency'] = value
                with self.assertRaisesRegex(ValueError, 'currency'):
                    calculator.calculate(data)

    def test_rounding_is_independent_of_ambient_context(self):
        data = single('100', '1.00005')
        results = []
        for ambient in (ROUND_UP, ROUND_DOWN):
            with localcontext() as context:
                context.prec = 4
                context.rounding = ambient
                results.append(calculator.calculate(data))
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[0]['precise_total_amd'], '100.00500')
        self.assertEqual(results[0]['rounded_total_amd'], '100.01')
        data['rounding']['per_receipt'] = 'half_even'
        self.assertEqual(calculator.calculate(data)['rounded_total_amd'], '100.00')

    def test_precise_and_receipt_rounded_totals_are_distinct(self):
        data = single('1', '0.005')
        data['payments'].append(dict(data['payments'][0], transaction_ref='SYN-SECOND'))
        result = calculator.calculate(data)
        self.assertEqual(result['precise_total_amd'], '0.010')
        self.assertEqual(result['rounded_total_amd'], '0.02')

    def test_strict_ambient_traps_and_exponent_limits_do_not_leak(self):
        data = single('10000', '250', '3')
        data['tax_rate'] = '0.0123456789'
        data['rounding']['tax'] = 'half_up'
        expected = calculator.calculate(data)
        expected_report = calculator.render(expected)
        with localcontext() as context:
            context.prec = 4
            context.Emax = 5
            context.Emin = -5
            context.traps[Inexact] = True
            context.traps[Rounded] = True
            actual = calculator.calculate(data)
            actual_report = calculator.render(actual)
        self.assertEqual(actual, expected)
        self.assertEqual(actual_report, expected_report)

    def test_small_quote_unit_does_not_overflow_rounding_precision(self):
        data = single('9' * 28, '9' * 28, '0.' + '0' * 95 + '1')
        result = calculator.calculate(data)
        self.assertEqual(Decimal(result['rounded_total_amd']),
                         Decimal(result['precise_total_amd']))

    def test_declaration_and_tax_rounding_are_explicit(self):
        data = single('1', '100.5')
        for policy, expected in (('truncate', '100'), ('half_even', '100'), ('half_up', '101')):
            with self.subTest(policy=policy):
                data['rounding']['declaration'] = policy
                self.assertEqual(calculator.calculate(data)['whole_dram_income'], expected)
        data['tax_rate'] = '0.5'
        data['rounding']['tax'] = 'half_up'
        self.assertEqual(calculator.calculate(data)['estimated_whole_dram_tax'], '51')
        data['rounding']['tax'] = 'half_even'
        self.assertEqual(calculator.calculate(data)['estimated_whole_dram_tax'], '50')

    def test_tax_rate_is_optional_and_has_no_default(self):
        self.assertNotIn('estimated_whole_dram_tax', calculator.calculate(single()))
        data = single()
        data['tax_rate'] = '0'
        with self.assertRaisesRegex(ValueError, 'tax'):
            calculator.calculate(data)
        data['rounding']['tax'] = 'truncate'
        self.assertEqual(calculator.calculate(data)['estimated_whole_dram_tax'], '0')
        for value in ('1.01', 0.01, True):
            with self.subTest(value=value):
                data['tax_rate'] = value
                with self.assertRaises(ValueError):
                    calculator.calculate(data)

    def test_empty_receipts_need_confirmation(self):
        data = single()
        data['payments'] = []
        with self.assertRaisesRegex(ValueError, 'zero_receipts_confirmed'):
            calculator.calculate(data)
        data['zero_receipts_confirmed'] = True
        result = calculator.calculate(data)
        self.assertEqual(result['whole_dram_income'], '0')
        self.assertEqual(result['currency_totals'], {})

    def test_missing_required_fields_and_wrong_shapes(self):
        for field in ('basis', 'rate_date_rule', 'rounding', 'payments'):
            with self.subTest(field=field):
                data = single()
                del data[field]
                with self.assertRaisesRegex(ValueError, 'Missing required field'):
                    calculator.calculate(data)
        for value in ([], None, 'not an object'):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculator.calculate(value)

    def test_required_fx_evidence(self):
        for field in ('transaction_ref', 'rate_date', 'rate_amd', 'rate_unit', 'rate_source', 'verified_on'):
            with self.subTest(field=field):
                data = single()
                del data['payments'][0][field]
                with self.assertRaisesRegex(ValueError, 'Missing required field'):
                    calculator.calculate(data)
        data = single()
        data['payments'][0]['rate_source'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'HTTP'):
            calculator.calculate(data)

    def test_unknown_rounding_does_not_silently_default(self):
        for field in ('per_receipt', 'declaration'):
            data = single()
            data['rounding'][field] = 'bank default'
            with self.assertRaises(ValueError):
                calculator.calculate(data)
        data = single()
        data['rounding']['unrecognized'] = 'truncate'
        with self.assertRaisesRegex(ValueError, 'Unknown rounding'):
            calculator.calculate(data)

    def test_input_is_not_mutated(self):
        data = sample()
        before = copy.deepcopy(data)
        calculator.calculate(data)
        self.assertEqual(data, before)

    def test_report_escapes_untrusted_text(self):
        data = single()
        data['basis'] = '<script>alert("basis")</script>'
        data['payments'][0]['transaction_ref'] = '<img src=x onerror=alert(1)>'
        data['payments'][0]['payer'] = '<script>alert("payer")</script>'
        data['payments'][0]['memo'] = '<script>alert("memo")</script>'
        report = calculator.render(calculator.calculate(data))
        self.assertNotIn('<script>', report)
        self.assertNotIn('<img ', report)
        self.assertIn('&lt;script&gt;', report)
        self.assertIn('&lt;img ', report)
        self.assertIn('Payer: &lt;script&gt;', report)
        self.assertIn('Memo: &lt;script&gt;', report)

    def test_report_shows_rate_source_and_statement_evidence(self):
        data = single()
        data['payments'][0]['rate_source'] = 'https://example.org/synthetic-rates?q=1&unit=1'
        report = calculator.render(calculator.calculate(data))
        self.assertIn('href="https://example.org/synthetic-rates?q=1&amp;unit=1"', report)
        self.assertIn('Payer: Synthetic Example Customer', report)
        self.assertIn('Statement page: 1', report)
        self.assertIn('Memo: Invented example; not a real payment', report)

    def test_report_never_links_a_non_http_source(self):
        result = calculator.calculate(single())
        result['payments'][0]['rate_source'] = 'javascript:alert(1)'
        report = calculator.render(result)
        self.assertNotIn('href="javascript:', report)


class IncomeCliTests(unittest.TestCase):
    def test_utf8_outputs_and_private_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / 'input.json'
            target = folder / 'private' / 'result.json'
            report = folder / 'private' / 'report.html'
            data = sample()
            data['basis'] = 'Սինթետիկ օրինակ'
            source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(target),
                                        '--html', str(report)], text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(target.read_text(encoding='utf-8'))['basis'], data['basis'])
            self.assertIn(data['basis'], report.read_text(encoding='utf-8'))
            if os.name == 'posix':
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(report.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(target.parent.stat().st_mode), 0o700)

    def test_cli_validation_error_is_clean_and_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source, target = folder / 'input.json', folder / 'result.json'
            data = single()
            data['quarter'] = 1.5
            source.write_text(json.dumps(data), encoding='utf-8')
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(target)],
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, 2)
            self.assertIn('quarter must be an integer', completed.stderr)
            self.assertNotIn('Traceback', completed.stderr)
            self.assertFalse(target.exists())

    def test_cli_refuses_to_overwrite_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.json'
            content = json.dumps(sample())
            source.write_text(content, encoding='utf-8')
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(source)],
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(source.read_text(encoding='utf-8'), content)

    def test_nonstandard_json_nan_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.json'
            target = Path(directory) / 'result.json'
            source.write_text('{"amount":NaN}', encoding='utf-8')
            completed = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(target)],
                                       text=True, capture_output=True)
            self.assertEqual(completed.returncode, 2)
            self.assertIn('NaN and infinity', completed.stderr)
            self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
