---
name: armenia-tax-turnover-election
description: Check eligibility and prepare or file Armenian form 201 electing turnover tax for an individual entrepreneur, including annual renewal, registration, conditional restart, re-registration, and microenterprise transitions. Use for choosing or renewing this tax regime; quarterly turnover calculations, annual returns, and payments have separate workflows.
---

# Turnover-tax election

Handle form **201 — «Հայտարարություն՝ շրջանառության հարկ վճարող համարվելու վերաբերյալ»** in Chrome at https://file-online.taxservice.am/ through the available browser tool. Verify the displayed taxpayer against the user's session context or explicitly supplied private profile. Restore authentication with `armenia-tax-login` if available. Do not store taxpayer identity or evidence in this public skill package.

Read [references/eligibility-and-deadlines.md](references/eligibility-and-deadlines.md) to select the legal case and check eligibility for the requested year. Before acting in the portal, read [references/portal.md](references/portal.md). The form number is publicly verified; form-specific live controls have not been verified. Inspect the current catalog, form help, and visible controls instead of inventing selectors or assuming quarterly form 286 behaves identically.

If browser tools or authentication are unavailable, produce the source-based eligibility/date worksheet and identify the remaining portal checks. Report that it is unsaved; do not claim that a portal draft exists.

## Establish the election

1. Identify the requested tax year, taxpayer status, current regime, registration/re-registration date, and any documented suspension/resumption or loss of microenterprise status. Select the **statutory case, effective date, and filing deadline separately**. An ordinary annual election is effective January 1 and due by February 20 inclusive. A later start date cannot repair a missed ordinary deadline. Restart has a conditional statutory window, not a universal exception.
2. Verify the rules effective for that case and year using current SRC guidance and ARLIS. The checked rules are dated 2026-10-05; already enacted declaration changes take effect on January 1 and February 1, 2027. Resolve an applicable amendment before using a prior form's attestations. Do not assume weekends extend an election deadline without authoritative confirmation.
3. Reconcile statutory prior-year sales turnover across **all activities** against filings and supporting records; the ordinary threshold is **not more than AMD 115 million**. A net bank receipt total or taxable profit is not automatically the sales-turnover total. Verify excluded activities, related parties, and contract arrangements against actual evidence. Ask for missing material facts before making an unsupported attestation. A past accepted election does not prove present eligibility.
4. Check filed/accepted declarations first, then completed and unfinished reports for the **exact taxpayer, form, tax year, and effective period**. If already accepted, retrieve its documents and verify the applicable status rather than filing another copy. An accepted filing can leave a retained unfinished copy. Reuse an authorized matching draft at its present stage; a correction requires explicit correction scope.
5. Prepare the date and required attestations from verified evidence. Form 201 chooses the regime; it does not select a universal activity rate. Do not add a default software classification or 1% rate. Election also does not establish a general VAT exemption for every transaction; assess any separate VAT obligation under its own applicable rule.
6. Save the draft using the current form's supported temporary-save control. Reopen and compare the persisted taxpayer, form/version, year, effective date, and all declarations with the reviewed case. Preserve the draft and private evidence of the eligibility check. Report the chosen case, effective date, statutory cutoff, saved status, and unresolved facts. A draft request ends with an unsigned saved draft.

Eligibility continues during the year: crossing the current-year sales threshold or beginning an excluded activity can end turnover-tax status. If evidence shows such an event, establish the applicable exit date and required notification instead of trying to preserve the regime with another election.

## File when requested

Complete the concrete reviewed declaration before any binding action. File only when the user requested filing of this election; follow the current browser tool's action-time confirmation and signing handoff requirements. A skill invocation or a draft request does not authorize filing. Keep phone PINs and OTPs with the user.

After submission, verify accepted/valid status for the exact taxpayer, form, year, and effective date. Retrieve the filed declaration and acceptance receipt into private storage outside the public repository. Verify that their identity, effective period, filing reference, and time agree. A saved draft, completed report, or signature alone does not establish acceptance.

If signing/submission is interrupted or its outcome is unknown, inspect completed reports and the filed archive before retrying. Reuse a matching signed report without issuing another signing challenge. Stop submission attempts once acceptance is established. If status remains ambiguous, preserve the page and report the uncertainty. A failed document download calls for retrieval, not resubmission.
