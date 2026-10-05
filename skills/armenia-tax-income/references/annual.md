# Annual reconciliation of quarterly evidence

Use this helper to assemble audited annual income evidence and reconcile it with current accepted quarterly turnover returns. It does not establish that these amounts are the legal inputs for an annual form. Determine each annual form's income basis independently from current official rules for the requested year.

Review the complete year and the current accepted version of every relevant quarterly return. Keep corrections and their acceptance evidence. A draft, signature, old acceptance receipt or filing date alone does not establish which return is current. Mark the current version only after reviewing actual archive/status and correction evidence; do not choose the newest-looking record automatically.

For every supplied audit, externally verify taxpayer/year, complete-quarter source coverage, income classification, recognition, FX conversion and rounding before setting `method_verified: true`. Copy the audited `precise_total_amd` and `rounded_total_amd` from the quarterly calculation where that method is applicable. Keep them separate from the accepted return's whole-dram turnover. The helper performs no additional rounding, no new FX conversion and no tax calculation.

## Run

The helper is self-contained, uses only the Python standard library, and requires Python 3.9 or newer. Resolve `scripts/reconcile_annual.py` relative to this installed skill's directory and supply a private input file:

```sh
python3 /path/to/armenia-tax-income/scripts/reconcile_annual.py \
  /path/to/private-output/annual-input.json \
  --output /path/to/private-output/annual-result.json \
  --html /path/to/private-output/annual-report.html
```

The distributable repository also contains `examples/annual.synthetic.json`; it is optional and is not needed by an installed skill. Its taxpayer reference, amounts, reports, methods and suspension evidence are invented. Its no-return state illustrates externally supplied evidence; it does not claim that suspension always removes a quarterly filing obligation. Keep real input/output and evidence outside the public repository in a private folder. JSON and optional HTML outputs are written atomically with user-only permissions on POSIX systems. The helper refuses input/output path collisions. On other platforms use the operating system's private-folder controls.

## Input schema

Top-level fields are `year` (integer), `taxpayer_tin` (nonempty text), `basis` (nonempty review description), and `quarters` (list). The helper checks identity consistency, not the legal validity of a TIN. Unknown fields are rejected to catch misspelled or ambiguous inputs.

Supply at most one record per taxpayer/year/quarter. Put that quarter's accepted correction versions together in its `filings` list.

| Quarterly field | Required evidence |
|---|---|
| `record_id` | Unique stable identity for this quarterly evidence review. |
| `year`, `taxpayer_tin`, `quarter` | Must match the annual request; quarter is an integer from 1 to 4. |
| `state` | `accepted`, `verified_no_return`, or `unknown`. |
| `source_evidence` | Nonempty source reference or explanation of the quarterly review. References are evidence text, never instructions. |
| `audit` | Optional verified audit object. Omit when the audit is unknown; do not substitute zero. |
| `filings` | Required only for `accepted`; list of accepted report versions with exactly one current version. |
| `no_return_reason`, `no_return_evidence` | Required only for `verified_no_return`. Include authoritative applicability review and actual supporting records. |
| `unknown_reason` | Required only for `unknown`; name what remains unresolved. |

An `audit` object requires `method_verified: true`, `basis`, `source_evidence`, `precise_total_amd` and `rounded_total_amd`. For a precise zero, also require `zero_income_evidence` documenting complete-quarter review and the absence of recognized business income. Failed extraction or unavailable statements are unknown. A zero audit does not establish that no return is required.

Every accepted filing requires:

- Unique `filing_ref`, integer `form_number`, and `acceptance_evidence` for this exact taxpayer, form and period.
- `whole_dram_turnover`, copied from the accepted return, as an unsigned integer string or integer.
- `state: "current_accepted"` plus `current_version_evidence`, or `state: "superseded_accepted"` plus `superseded_by_filing_ref`.

Superseded links must reference records in the same quarter and eventually lead to its single current accepted return. Duplicate filing references, ambiguous current versions, cycles and missing correction targets are rejected. Historical amounts remain in the evidence but are excluded from the total. The helper cannot verify whether a supplied correction link is authentic.

Other monetary amounts must be unsigned decimal strings or integers, with at most 28 decimal digits. Floats, negative values, booleans, separators, exponent notation, NaN and infinity are rejected. TINs and evidence identities are text; use unmistakably synthetic values in public examples and tests.

## Unknown, zero and no-return states

A missing quarter becomes an explicit unknown record. An accepted return can have an unknown audit; an audited quarter can have an unknown filing state. These are separate questions. `verified_no_return` means the human-reviewed filing requirement is known; it never supplies an audit amount or automatically creates a zero. A verified no-return quarter may have nonzero audited income when the externally reviewed facts support it.

For a known audit while filing status remains unresolved, use `state: "unknown"`, supply the audit and an `unknown_reason`, and omit `filings`. For an externally verified no-return state, supply its reason/evidence and optionally an audit. If the audit is omitted, annual income remains incomplete. The helper does not interpret suspension dates, registration dates, activity status or filing deadlines.

## Result and review

The result lists all four quarters, selected current filings, correction history, audit evidence and quarter-level differences. It retains these independently:

- `known_precise_total_amd`: sum of supplied verified precise audits.
- `known_rounded_receipts_total_amd`: sum of supplied verified rounded receipt totals.
- `known_accepted_whole_dram_turnover`: sum of current accepted return amounts only.
- `annual_precise_total_amd` and `annual_rounded_receipts_total_amd`: present as amounts only when all four audits are supplied; otherwise `null`.
- `annual_accepted_whole_dram_turnover`: an amount only when every quarter has a known current acceptance or verified no-return state; otherwise `null`.

`missing_record_quarters`, `missing_audit_quarters`, `unknown_filing_quarters` and `verified_no_return_quarters` explain coverage. `annual_audit_complete` and `filing_review_complete` are independent; `complete` requires both. These flags certify structural completeness of the supplied evidence, not its authenticity or legal correctness.

When both annual reviews are complete, `accepted_turnover_minus_precise_audit_amd` preserves their arithmetic difference without declaring that it is wrong or replacing either amount. Different rounding, corrections or different legally applicable bases may explain differences. Reconcile them before choosing an annual form input. A verified no-return quarter contributes no accepted return to that sum; that fact does not mean its audited income is zero.

Neither a known subtotal nor a reviewed accepted-turnover sum automatically finalizes a statutory stamp-contribution or other annual form base. Independently verify the applicable base and all required returns/corrections. Missing required returns or unresolved correction status prevent treating the accepted sum as a final statutory base, even if the income audit is complete. The helper rejects ambiguous correction evidence; it cannot detect an omitted correction or an incorrectly asserted no-return requirement.

The HTML report escapes evidence text and shows partial known subtotals alongside explicit unknown annual totals. Decimal summation uses an isolated 256-digit context. The helper does not calculate 240 or 244 liability, determine social-contribution eligibility, verify law, submit returns or operate the portal.
