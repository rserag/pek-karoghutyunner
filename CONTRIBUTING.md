# Contributing

Keep each skill focused on its outcome. Put observed controls and longer explanations in `references/`; executable arithmetic belongs in the income helper. Changes to dates, tax treatment, deadlines, or receiving accounts need an authoritative source and the reporting period to which it applies. A past portal observation is a navigation hint, not a universal legal rule.

## Privacy before publication

- Use invented test data. Do not contribute statements, taxpayer names/numbers, login identifiers, phone numbers, employer details, filing IDs, payment history, screenshots, cookies, tokens, or personal filesystem paths.
- Keep private profiles and evidence outside the checkout. Inspect `git diff --cached` and `git status` before committing. Do not copy a private skill's references into a public change.
- If reporting a portal issue, describe the label, page, and behavior using redacted or synthetic details. Do not include full URLs with authentication query tokens.

## Checks

Run `python3 scripts/check_package.py` and `python3 -m unittest discover -s tests -v`. Introduce a regression test for an arithmetic bug, especially one involving input identity, conversion units, dates, rounding, or annual correction/completeness handling. Keep the helpers free of taxpayer-specific defaults and network dependencies. Validate changed skills with the available skill validator as well; structural checks do not replace realistic workflow evaluation.

Review changed workflow instructions against these scenarios without executing a real filing or payment merely to test them:

| Scenario | Expected behavior |
|---|---|
| Another taxpayer's session is open | Stop and restore the correct account before tax work |
| The same receipt appears on two statement pages | Reconcile identity; count it once |
| Recognition differs from receipt date | Use another reviewed calculation; do not relabel receipt-date arithmetic |
| Rate is quoted per 100 currency units | Divide by the verified quote unit and show it in the report |
| Draft totals initially show zero | Save, reopen, and verify persisted portal totals |
| Accepted filing also has an unfinished copy | Retrieve acceptance; do not submit the retained copy |
| Signing/submission is interrupted | Check completed reports and archive before retrying |
| Newly accepted tax is beyond the statement cutoff | Show it separately until posting, then match and count once |
| Several liabilities share unified credit | Apply that credit once across eligible liabilities |
| A separate stamp/admin credit exists | Keep it separate from ordinary unified tax credit |
| Bank says paid but treasury has not posted | Check receipt/cutoff/posting before another transfer |
| Treasury credited money but liability is unsettled | Distinguish funding from allocation and verify settlement |
| Annual quarters are missing or duplicated | Identify the incomplete year or reject duplicates; do not silently use zeros or double count |
| A quarter has an accepted correction | Use verified current/superseded links and count that quarter once |
| Annual bank total differs from accepted quarterly turnover | Preserve both totals, explain the difference, and use the legally required source for each field |
| Formal suspension excludes full profit-tax months | Calculate profit months from Article 125 evidence and determine social months independently |
| The 244 annual version after July 2026 is unresolved | Preserve the worksheet and verify official annual applicability before finalizing affected fields |
| Social contribution is exempt but stamp contribution applies | Assess both independently; a social exemption does not suppress the annual stamp check |
| Annual liability was prepaid or is not posted yet | Preserve gross declared liability and reconcile payments/posting separately without counting it twice |
| Ordinary 201 election deadline was missed | Check genuine statutory alternatives; do not invent a later effective date |
| Resumption occurs after February 20 | Verify the conditional restart case from actual activity/suspension history |
| Turnover is within the limit but an activity is excluded | Resolve eligibility before attesting or preparing an election for filing |
| A new year has an enacted form/rule change | Verify its effective date and applicable year/case before reusing old attestations or amounts |

Browser tool policies and user authorization govern live actions. A package test cannot establish legal eligibility, permission to sign, treasury posting, or actual payment settlement.

For substantial annual/election workflow changes, use an independent synthetic forward-test when available. Ask the evaluating agent to work through realistic requests with the skill and raw evidence, without giving the intended answer. Do not execute a real filing or payment merely to test instructions.
