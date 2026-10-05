---
name: armenia-tax-declaration
description: Prepare and verify an Armenian quarterly turnover-tax declaration in Chrome using prior filings and an audited income calculation. Use for a saved draft or explicitly requested filing. Verify the applicable form, categories, and rates for the taxpayer and period; income extraction and login have separate skills.
---

# Quarterly turnover-tax declaration

Use Chrome at https://file-online.taxservice.am/ through the available browser tool. Verify the displayed taxpayer against the user's session context or explicitly supplied private profile. Restore authentication with `armenia-tax-login` if available. Read [references/portal.md](references/portal.md) for observed form 286 controls, draft verification, and submission recovery. Inspect current controls before acting.

## Prepare a reviewable draft

1. Obtain a finalized, auditable calculation for the requested quarter. Record recognition basis, exchange-rate rule, exact AMD total, and whole-dram treatment. Verify taxpayer status, activities, applicable form/version, income categories, activity codes/shares, rates, exemptions, and deductions against actual evidence and current official rules effective for that period. Prior filings are useful examples, not proof of continued eligibility. Do not assume software services, a special rate, or a particular form row.
2. Check accepted/filed reports first, then completed and unfinished reports for the same taxpayer, form, year, and quarter. An accepted filing may leave a retained unfinished copy. If already accepted, retrieve its documents and report status; a correction requires explicit correction scope. Otherwise reuse the authorized existing draft or completed report at its current stage. Leave unrelated drafts alone.
3. Select form, year, and quarter. Resolve the period-change confirmation **before** entering amounts, because changing periods can clear the form. Enter whole dram according to current form guidance. Fill only applicable categories and verify the activity breakdown. Let the portal calculate readonly tax/totals; a helper's estimate does not replace them.
4. Use **Հիշել Ժամանակավորապես** for a draft. Reopen it and verify persisted period, income, tax, totals, and activity code/share against the calculation. In the observed form, saving and reopening refreshed calculated totals that initially displayed zero. Never manually write readonly fields or report persistence from an in-memory input alone.
5. Preserve evidence in a private location outside the public repository. Report the period, exact conversion total, saved whole-dram income and tax, applicable categories/rate, activity breakdown, saved status, and material assumptions. Preserve the live draft for review. A draft request ends with an unsigned saved draft.

## File when requested

Complete the concrete declaration review before signing or submission. The user must have requested filing of this declaration; follow the browser tool's current action-time confirmation and signing handoff requirements. Routine skill invocation or draft preparation does not authorize a legally binding filing. Phone PINs and OTPs remain with the user.

After filing, verify accepted/valid status for the exact taxpayer, form, and period. Retrieve the filed copy and acceptance receipt and report their private locations. A signature alone does not establish acceptance.

If signing/submission is interrupted or its outcome is unknown, inspect completed reports and the archive before retrying. Reuse a matching signed report without issuing another signing challenge. Stop submission attempts once acceptance is established. If status remains ambiguous, preserve the page and explain the uncertainty. A failed receipt download calls for retrieving documents, not resubmitting the declaration.

Filing and payment are distinct actions. Review debt and funding needs with `armenia-tax-balances` if requested; execute a payment only within separate payment authorization and the tool's financial handoff rules.
