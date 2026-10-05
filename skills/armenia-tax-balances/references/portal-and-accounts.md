# Portal balances and receiving accounts

Observed on 2026-10-04 and 2026-10-05; portal version 3.70.0 was observed on 4 October. Refresh figures, notices and account mappings for each review. These UI observations are not standing payment instructions.

## Navigation

From **Անձնական գրասենյակ** (Personal office), use **Հարկային պարտավորություններ** (Tax liabilities). Choose the pre-2025 or post-2025 ledger applicable to the records being reviewed.

| Visible label | Meaning | Observed route |
|---|---|---|
| ԱՀՔ դիտում | Personal-account ledger | `/pages/ledgerPacView.jsf?pId=1&tId=7&versionSelect=true` |
| Միասնական հաշիվ | Unified deposits and allocations | `/pages/ledgerUnifiedAccount.jsf?pId=1&tId=7` |
| ԱՀՔ քաղվածք | Statement across tax categories | `/pages/ledgerPacRemainders.jsf?pId=1&tId=7` |
| Տույժերի պատմություն | Late-payment charge history | `/pages/ledgerFineHistory.jsf?pId=1&tId=7` |
| Տուգանքների պատմություն | Fine history | `/pages/ledgerPenaltyHistory.jsf?pId=1&tId=7` |
| Մարում / վերադարձ | Settlement/refund workflow | `/pages/repaymentOrder.jsf?pId=1&tId=7` |
| Վճարումներ | Treasury payment search | `/pages/treasuryPayments.jsf?pId=1&tId=3` |
| Էլեկտրոնային վճարումներ | Payment-order search | `/pages/electronicPayment.jsf?pId=1&tId=12` |

Routes are hints from observed links. If a sidebar click leaves the view unchanged, inspect its visible href and navigate normally to that observed route rather than repeating blind clicks. **Հարկատեսակների ԱՀՔ** is the ordinary ledger; **Վարչական ակտի ԱՀՔ** is the administrative-act ledger, observed with `isAudit=true`. Keep them separate.

## Queries and accounting interpretation

- Statement: fill **Մնացորդ առ** (as-of date), then **Դիտել**. The observed footnote said the underlying records were from the day before generation. Record the current footnote's actual cutoff separately from the selected date. A portal trial-operation notice also said records may be corrected and discrepancies should be raised with SRC taxpayer services; check whether that notice remains applicable.
- Unified account and histories: choose start/end dates and **Ցանկացած** (all tax types), then **Դիտել**. Widen the period when the opening balance or a material movement is unexplained.
- Tax ledger: select tax/date and query, then inspect the selected year and quarter filters. A tested query showed headers without entries until year and quarter **Բոլորը** were selected. Two controls can both say Բոլորը; derive the intended one from its current visible grouping.
- A selected-year footer can say 31 December during a query earlier in the year. It is not the data freshness date.
- A per-tax ledger may show common deposits but omit allocations to other taxes, producing a misleading running unified balance. Use the all-tax unified history and statement to establish available funds; do not sum per-tax running balances.
- **Տույժ** means a late-payment charge; **տուգանք** means a fine. Historical assessed amounts need not remain outstanding. Compare **Մարված** (settled), reductions and remaining balances.
- The statement distinguishes not-yet-overdue (**Ոչ ժամկետանց**) and overdue (**Ժամկետանց**) amounts, and ordinary versus administrative assessments. Its total already includes relevant components; do not add the total to them again.
- Credit headings can be merged across columns. Read all heading levels before assigning a number to debit/reimbursement balances, tax-specific overpayments, ordinary unified funds or administrative-act funds. **Սահմանված չափից ավել վճարած գումարներ** includes earmarked social, stamp, insurance and duty subcolumns. **Միասնական հաշվում առկա գումար** is separate from administrative-act funds. Do not net restricted credit against another account's liabilities.
- Whole-AMD movement arithmetic can differ from the corroborated statement balance. Preserve a discrepancy, inspect available finer precision and avoid asserting hidden fractions as its explanation without evidence. Do not replace a confirmed portal balance with a reconstructed amount silently.
- Treasury payment search yielded no usable rows during one review although the unified history showed credited deposits. An empty or unresponsive legacy search is not proof that no payment exists.

## Posting and allocation lessons

The 4–5 October observations showed why declaration, bank payment, treasury credit and allocation must be reviewed separately:

- A newly accepted quarterly declaration can be absent from a previous-day statement and appear on a later review. Check the archive and count a matched liability only once when it posts.
- A declared liability can be recorded as not yet overdue while unified funds remain available and the liability has not been settled. Available money is not proof of allocation, and zero overdue debt is not zero unpaid tax.
- A taxpayer-reported treasury transfer was not yet visible in the records reviewed. A missing entry, especially beyond the statement cutoff, does not establish a failed bank payment. Inspect the bank receipt, amount, date, taxpayer identity, receiving account and execution status before suggesting another transfer.
- Do not count a processing or bank-paid transfer as available portal credit until treasury posting is verified. Do not recommend duplicating it merely because the portal has not updated.
- A payment memo naming a quarter does not establish that the treasury allocated funds to that quarter. Reconcile deposit history with the refreshed liability and settlement records.

## Tax categories

The statement is a broad catalog, not a list of taxes necessarily applicable to the user. It includes turnover tax (**Շրջանառության հարկ**); income tax (**Եկամտային հարկ**); profit tax (**Շահութահարկ**); domestic/import VAT (**ԱԱՀ**) and excise; monthly/annual social payments; mandatory stamp contribution (**Դրոշմանիշային վճար**); insurance premium (**Ապահովագրավճար**); state duties; royalties; environmental/resource/road charges; regulatory fees; fines/damages; and legacy categories.

A zero row means no recorded balance in that view, not an exemption or proof that future obligations are settled. An annual applicability review for an individual entrepreneur may require year-to-date business income, taxpayer regime/status, activity and active months, pension/social status, employees and other income. Use current SRC guidance and the law effective for the relevant period before asserting obligations, rates, deadlines or exemptions.

## Receiving accounts and official sources

Mappings were corroborated on 2026-10-04. Reopen the official source or a current portal account directory before giving payment instructions.

| Purpose | Treasury account | Official source |
|---|---|---|
| Ordinary tax unified account, including ordinary turnover-tax funding | **900008000490** | [SRC annual report, 2025 settlement-system discussion](https://www.src.am/storage/annualActivityReports/hv_gorts_tarekan_2024_68010359e488a.pdf); [Finance treasury specification](https://minfin.am/website/images/files/2c3d99a2.pdf) |
| Administrative-act unified account | **900008000771** | [SRC report, separation from 2025](https://www.src.am/storage/annualActivityReports/hv_gorts_tarekan_2024_68010359e488a.pdf) |
| Mandatory stamp contribution | **900005001186** | [ZINAPAH mandatory-payment instructions](https://zinapah.am/en/mandatory-payment) |

Ordinary/administrative numbers were corroborated through official indexed documents, not displayed as payee instructions on the observed portal statement. Large SRC PDFs may fail to open in a web tool. State the actual source level and do not claim live portal payee verification if it was not performed.

ZINAPAH identifies the mandatory account as held at the Ministry of Finance Central Treasury, with State Revenue Committee as recipient. Voluntary donation accounts are different. The Finance specification is technical documentation; its internal transit/control accounts are not replacement payment destinations.

Use the reviewed taxpayer's verified name and TIN in the bank's payer/taxpayer fields. Keep these separate from beneficiary identifiers. Verify mandatory bank fields against the actual form or official instructions; do not guess beneficiary TIN, IBAN, SWIFT or other details.

The observed legal source described quarterly turnover tax as due by the 20th of the following month under Tax Code Article 262. Verify the version and date conventions applicable to the requested period before giving a deadline. Official entry points: [ARLIS Tax Code](https://www.arlis.am/hy/acts/215611), [latest-version route previously used](https://www.arlis.am/hy/acts/201478/latest).

## Electronic order statuses and action boundaries

[Portal help](https://file-online.taxservice.am/help/elPaymentHelp.html) distinguishes **Չստորագրված** (unsigned), **Ստորագրված** (signed), **ընթացքում / Ընթացքում** (processing), **Չուղարկված** (not sent), **Սխալ** (error), **Մերժված** (rejected), and **Բանկի կողմից վճարված** (paid by bank). Verify current help if a status has changed or is ambiguous.

Creation, signing, sending, bank execution, treasury credit and liability allocation are separate stages. Search existing orders before any later payment workflow. Reviewing balances or suggesting payment details does not authorize creating, signing, sending or retrying an order; early settlement; refunds; or cross-account transfers. During a review do not click **Ստեղծել վճարման կարգադրություն**, transaction-confirmation controls or settlement/refund actions. A later authorized financial request still requires the current browser tool's user handoff at execution.
