# Verified inputs and portable arithmetic

This package supplies no taxpayer profile, income recognition method, tax rate, FX-date rule, or rounding convention. Establish those for the actual taxpayer, activity, form, and reporting period before setting `method_verified` to `true`. User preference alone does not establish the legally applicable method.

## Evidence before arithmetic

Confirm statement coverage of the complete quarter, including continued rows on adjacent pages. Record receipt/value dates, credit amount, currency, payer, memo, source page, and the bank transaction identifier. Explain which date determines recognition and why. Distinguish genuine business receipts from debits, opening balances, own-account transfers, and zero-foreign-currency revaluation rows. Resolve ambiguous credits; do not silently exclude or include them.

This helper supports quarter membership and FX-date comparisons against `receipt_date` only. If the legally verified basis requires an invoice, service, accrual, or other recognition date, stop and use a separate reviewed calculation. Changing the `basis` label does not change the helper's date logic.

For foreign receipts, verify historical CBA rates through the [rate.am Central Bank archive](https://www.rate.am/hy/armenian-dram-exchange-rates/central-bank-armenia), with the [official CBA retrieval page](https://www.cba.am/en/exchange-rates-retrieval) as a cross-check. Verify the currency, quote unit, and publication date. Check the [Tax Code and amendments on ARLIS](https://www.arlis.am/) effective in the reporting period before selecting the rate-date rule. A preceding calendar date is not proof of the preceding working day's publication. Commercial bank buy/sell quotes are not CBA rates.

Record the applicable income and tax rounding requirements from the form or another authoritative source. A previous filing can support reconciliation but does not establish a universal rounding or tax rule. Compare calculated AMD amounts with bank equivalents and explain discrepancies rather than replacing verified rate arithmetic silently.

## Input schema

Run from the package root with Python 3.9 or newer; the helper uses only the standard library:

```sh
python3 skills/armenia-tax-income/scripts/calculate.py \
  examples/income.synthetic.json \
  --output /path/to/private-output/result.json \
  --html /path/to/private-output/report.html
```

The example contains invented dates, rates, amounts, and tax assumptions. Its choices demonstrate arithmetic and do not recommend a legal method.

Required top-level fields:

| Field | Meaning |
|---|---|
| `year`, `quarter` | JSON integers; quarter 1–4. Strings, booleans, and fractional values are rejected. |
| `basis` | Nonempty description of the verified recognition basis. |
| `method_verified` | Must be `true`, confirming external verification of recognition, FX timing, and rounding. The script cannot verify that claim. |
| `rate_date_rule` | `before_receipt`, `same_day`, or `on_or_before_receipt`. Checks date ordering only, not holidays, working days, publication schedules, or law. |
| `rounding.per_receipt` | `half_up` or `half_even` for each AMD conversion to two decimal places. |
| `rounding.declaration` | `truncate`, `half_up`, or `half_even` for the sum of rounded receipts to whole AMD. |
| `payments` | List of verified taxable receipts. |

Optional `tax_rate` is a fraction from 0 to 1, e.g. synthetic `"0.02"`. Supplying it requires `rounding.tax` (`truncate`, `half_up`, or `half_even`). The estimate applies the supplied rate to `whole_dram_income`; it does not model deductions, exemptions, minimums, or mixed activities. Omit the rate when that arithmetic is not the verified form calculation. No tax-rate default is supplied.

An empty list is allowed only with explicit `zero_receipts_confirmed: true` after verifying complete coverage and classification. It then produces zero income; it does not establish that filing is unnecessary.

Each receipt requires:

- `transaction_ref`: a stable, unique identifier across the supplied statement set. Prefer the bank's transaction ID. For multiple accounts, namespace it with a private account alias. If no ID exists, construct a documented identity from source evidence; resolve ambiguity before calculation. The same ID repeated on another page is rejected. Distinct transactions with identical dates and amounts remain separate when their IDs differ.
- `receipt_date`: a valid `YYYY-MM-DD` date within the requested quarter.
- `currency`: an uppercase three-letter currency code. The script checks its format, not an ISO registry or quote availability; verify the actual currency externally.
- `amount`: positive decimal string or JSON integer. Monetary JSON floats and booleans are rejected. Strings must use digits and an optional decimal point, without separators, signs, or exponent notation; at most 28 decimal digits are accepted.

Foreign receipts additionally require `rate_date`, positive `rate_amd`, positive `rate_unit`, an absolute HTTP(S) `rate_source`, and `verified_on`. For example, a rate of 250 AMD **per 100 JPY** is entered as `rate_amd: "250"`, `rate_unit: "100"`. Verification cannot predate the rate publication. Source authenticity and the actual value are external checks.

For `AMD`, omit all FX fields. The amount is already AMD and no publication-date condition applies.

Optional `payer`, `memo`, and positive integer `source_page` retain extraction evidence. Additional provenance fields may be retained in JSON; they are not independently verified. Do not include authentication secrets. Store real statements and generated reports outside the public repository.

## Results and limitations

The helper always rounds each receipt to two decimal places before rounding their sum to whole dram. If the verified rules require aggregate-only rounding or another intermediate policy, use a separate reviewed calculation instead of setting `method_verified` for an incompatible method.

`precise_amd` and `precise_total_amd` are conversion values before receipt rounding; divisions use an isolated, explicit 256-digit Decimal context, including independent traps and exponent limits. Repeating quotients remain approximations. `rounded_amd` and `rounded_total_amd` apply the requested receipt policy. `whole_dram_income` rounds the **sum of rounded receipts**, not the unrounded total. `currency_totals` retain separate native-currency totals. The optional `estimated_whole_dram_tax` is an arithmetic estimate, requiring portal verification before filing.

The HTML report shows both totals, quote units, publication/verification dates, all selected policies, safe HTTP(S) rate-source links, and any supplied payer, memo, or statement page as escaped text. It is explanatory evidence, not a declaration or payment instruction. Compare its whole-dram figure with the portal's saved calculation and stop on a material discrepancy.

The helper reads UTF-8, refuses to overwrite its input, writes outputs atomically with user-only file permissions on POSIX systems, and creates a private leaf output directory when needed. On platforms without POSIX permission enforcement, use the operating system's private-folder controls. Invalid input exits with code 2 and a concise error. It does not extract PDFs, fetch rates, validate working-day calendars, decide receipt eligibility, or operate the tax portal.
