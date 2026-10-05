---
name: armenia-tax-annual-returns
description: Prepare and verify annual Armenian forms 240 and 244 for an individual entrepreneur operating under turnover tax, separately or together, in Chrome. Use for an annual calculation, saved draft, or explicitly requested filing; regime election, quarterly turnover returns, personal income declarations, and payments are separate tasks.
---

# Annual turnover-tax entrepreneur returns

Handle only the forms and reporting year the user requested. This first version supports individual entrepreneurs whose relevant business activity is taxed under turnover tax. If evidence shows general taxation, mixed regimes, notarial activity, or an unresolved eligibility change, preserve the evidence and prepare what can be established; do not force the turnover-only treatment onto the unsupported portion.

Read [references/form-240.md](references/form-240.md) for form 240, [references/form-244.md](references/form-244.md) for form 244, and [references/portal.md](references/portal.md) when opening or writing a portal report. References record research checked on 2026-10-05, not permanent rules. Recheck official sources and their effective reporting periods before calculating a different year or filing. Select by Armenian title, reporting year, and version as well as form number.

## Establish the annual evidence

- Confirm taxpayer identity from the authenticated portal and the user's session context or explicitly supplied private profile. Obtain registration/closure dates, turnover-regime election and eligibility evidence, and submitted suspension/resumption declarations with submission dates. A prior return is an example of a past treatment, not proof of this year's status.
- Establish whether the user wants calculations, unsigned saved drafts, or filing. Check accepted reports first, then completed and unfinished reports for the exact taxpayer/form/year. Reuse a matching authorized draft. An existing accepted return requires explicit correction scope before preparing a replacement; a retained draft does not justify another submission.
- Keep a private annual worksheet with separate monthly columns for turnover-regime status, fixed profit-tax applicability, social-payment applicability, exclusions, and evidence. Determine profit and social months independently. Do not assume twelve months, copy profit-tax suspension exclusions into social calculations, or infer suspension from zero receipts. Resolve unknowns before entering their amounts.
- For form 244, establish social status separately: birth-date cohort, voluntary participation, residence/treaty treatment where relevant, pension age and any valid stopping application. Check any combined salary/business cap or adjustment that actually applies. Keep sensitive supporting data outside the distributable skill and public repository.
- For stamp-fee calculations, obtain the latest accepted original or corrective turnover return for every relevant quarter. Record report reference/status and annual sales turnover by quarter; count each quarter once. Reconcile discrepancies against the audited annual income evidence before calculating the fee. Bank deposits alone are not the filed-turnover base. Missing reports remain unknown, not zero.

When installed and available, use `armenia-tax-login` to authenticate, `armenia-tax-income` for missing receipt/conversion evidence, and `armenia-tax-balances` for a requested liability/payment review. They are optional helpers: this skill's own annual evidence and verification requirements still apply. Authentication uses the user's chosen supported method; PINs and OTPs stay with the user.

## Prepare and verify

Use Chrome at https://file-online.taxservice.am/ through an available browser tool. If no browser tool or authentication is available, complete the source-based worksheet and report the precise remaining portal check; do not claim a portal draft exists.

1. Verify current official form help, applicable version, deadlines and whole-dram treatment. For 244, resolve the July 2026 version transition before selecting stamp fields. Build the requested form's calculation from established evidence; previous payments do not reduce a gross liability field unless its instructions expressly provide a deduction.
2. Inspect current year/period controls. Resolve any period-change confirmation before entering amounts. Fill only supported applicable fields, and let the portal calculate readonly fields. Check displayed formulas against the worksheet rather than overriding them.
3. Save an unsigned draft using the current temporary-save control, then reopen that exact draft. Verify persisted taxpayer, form/version, year, applicable amounts, calculated totals and any social/stamp sections. A value visible before saving is not persistence evidence.
4. Report each requested form's status separately, the calculation/evidence summary, deadlines, unresolved issues and private draft/evidence locations. A draft request ends with a saved unsigned draft; if a required rule/version remains unresolved, preserve a worksheet or partial draft and state exactly which amount was not finalized.

## File only when requested

Complete concrete review of the exact requested report before signing/submission. Filing must be requested; follow the current browser tool's action-time confirmation and signing handoff requirements. A calculation request, skill invocation, or approval to install the skill does not authorize filing.

After submission, verify the accepted/valid archive state for the exact taxpayer/form/year and retrieve the filed copy and acceptance receipt. In a bundle, track each return independently; one accepted return does not establish the other's status. If an outcome is unknown, inspect completed reports and the archive before retrying. Reuse a matching signed report; stop once acceptance is established. A missing download calls for document retrieval, not resubmission.

Filing and payments are separate. Include estimated obligations and due dates in the review, but execute payments or early settlement/credit-return actions only under separate user authorization and the browser tool's financial handoff rules.
