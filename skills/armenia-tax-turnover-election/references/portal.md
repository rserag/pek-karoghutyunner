# Form 201 portal workflow and evidence

The [government Hartak service](https://hartak.am/services/2e560b1b-1bfd-4017-a180-72945fec90a0/online/) publicly verifies choosing **201** from the reports catalog, entering the date from which turnover-tax status is sought, and reviewing the eligibility declarations. Live form 201 inputs, selectors and signing controls have **not** been verified. On 2026-10-05 the available portal session was expired; no form 201 draft or submission was made during skill research.

Use Chrome at https://file-online.taxservice.am/ through the available browser tool. Inspect current labels and controls, and follow its current legal-signing/financial action requirements. Use `armenia-tax-login` if authentication must be restored. A saved private profile supplies expected identity and signing details; do not introduce a default identity or provider.

## Find existing work before creating a declaration

The following navigation was observed in other portal tax workflows, not independently tested for form 201:

| Purpose | Armenian label | Historical route hint |
|---|---|---|
| Catalog | Inspect the current catalog label | `/pages/declarationForms.jsf?pId=2&tId=1` |
| Unfinished drafts | Անավարտ հաշվետվություններ | `/pages/savedForms.jsf?pId=2&tId=2` |
| Completed reports | Լրացված հաշվետվություններ | `/pages/submittedForms.jsf?pId=2&tId=3` |
| Filed reports | Հանձնված հաշվետվություններ | `/pages/archiveForms.jsf?pId=2&fetchData=true&tId=4` |

Use current navigation; a historical route is a hint, not permission to replay a registration POST or guess a form endpoint. Check filed records first, then completed and unfinished lists. Match taxpayer, form 201, year and effective date/period. Inspect the filed document when list columns omit the effective date. **Վավեր** is a valid-status label; verify current acceptance rather than treating the completed list as proof of filing.

An accepted report may also have a retained unfinished copy. Retrieve the accepted document and receipt instead of submitting that copy. A matching unsigned/signed completed report should be resumed at its current stage within the requested scope. Leave unrelated work alone. Correcting an accepted election requires explicit correction scope and a verified legal route.

## Draft and verify persistence

- Select the current form/version for the target year. Review the form help and the current attestation text against the applicable legislation, including future amendments that have become effective.
- Resolve any date/year-change confirmation before filling attestations; period changes can discard values in other portal forms.
- Set the verified statutory effective date. Do not substitute today's date, a convenient date after a missed cutoff, or the bank's first-receipt date without a statutory basis.
- Fill attestations from evidence. If the form includes a declaration inconsistent with the case or verified eligibility, resolve the discrepancy before registering or signing.
- Use the current temporary-save control; **Հիշել Ժամանակավորապես** is the label observed in other workflows. Reopen the saved declaration and verify the persisted taxpayer, form/version, year, effective date and every material declaration. Report an actual saved draft rather than an in-memory filled form.

## Filing and interruption recovery

The portal's **Գրանցել** action in other workflows created a completed unsigned report; signing and sending were separate stages. Inspect the actual form 201 sequence before using it. Complete the reviewed draft before a binding action. Filing must have been requested, and the current browser tool's required action-time confirmation must be satisfied. Keep Mobile ID PINs and OTPs with the user.

Verify the exact row and document before a signing challenge or send action. If signing/submission times out, inspect completed reports and the filed archive before retrying. Reuse a matching signed report; do not duplicate a pending phone challenge. Once accepted, stop submission attempts.

After filing, obtain both the filed declaration and acceptance receipt from their current visible links. Derive document references from that accepted row, never a previous filing. Compare taxpayer, form, effective date/year, registration/electronic references and filing time. Store them in a private location outside the public repository and report those locations. If downloads fail, check whether files already arrived, then retry retrieval only. Ambiguous filing status requires preserving evidence and reporting uncertainty, not repeated submission.

The portal may offer additional liability-allocation or financial actions after a submission. Form 201 election does not authorize payments or other financial mutations; complete only the requested election workflow.
