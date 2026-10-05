---
name: armenia-tax-balances
description: Review Armenian tax-portal debt, credits, payment history, and receiving accounts in Chrome, and suggest how much to send to each account and by when. Income calculation, declaration filing, and executing payments are separate tasks.
---

# Armenian tax balances

Explain recorded liabilities, upcoming declared tax, eligible credits, and receiving accounts using current portal evidence and official sources.

## Review

Use Chrome at https://file-online.taxservice.am/ through the available browser tool. Verify the displayed taxpayer against the user's session context or an explicitly supplied private profile outside the public repository (`identity.tin`, and expected name/username where supplied). If authentication is needed, use `armenia-tax-login` when available. Ask for required missing context; do not reuse another taxpayer's identifiers.

Read [references/portal-and-accounts.md](references/portal-and-accounts.md) for tested navigation, Armenian labels, accounting pitfalls, and official account sources. Inspect current controls rather than treating old observations as current data.

1. Open **Հարկային պարտավորություններ** and choose the applicable ledger era. Generate **ԱՀՔ քաղվածք** for the requested date. Record both the selected date and the statement's actual data cutoff. Separate principal, late-payment charges, fines, overdue amounts, and amounts not yet overdue. Separate ordinary liabilities from administrative-act liabilities.
2. Read credits by their complete column headings, including merged headers. Distinguish ordinary unified-account funds, administrative-act funds, tax-specific overpayments, and debit/reimbursement balances. They are not one interchangeable credit pool.
3. Reconcile the statement with **Միասնական հաշիվ**, using all tax types and a period broad enough to explain the current balance. Deposits, allocations, refunds, and reversals are different events. Trace material liabilities to their tax-specific ledger and declaration reference. Use late-charge/fine histories when amounts need explanation.
4. Reconcile relevant accepted declarations against recorded liabilities by reference, especially current or unsettled periods, regardless of acceptance date. Use `armenia-tax-declaration` archive guidance if available. A declaration can remain unposted even when older than the statement cutoff; report unmatched accepted obligations separately without filing again or declaring the taxpayer debt-free. Use the cutoff to explain freshness, not to assume that all earlier declarations posted.
5. Explain relevant tax categories. A zero row means no recorded balance in that view, not that the category can never apply. For annual or other unassessed obligations, verify taxpayer status, activity, relevant year, and current official law before asserting applicability, rates, deadlines, or exemptions. Explain missing information without inventing debt.

## Amount and destination

Calculate a proposed funding gap only from liabilities and credits eligible for the same account. Use exact arithmetic on the available precision, apply each credit once, and avoid adding a displayed total to its components. Displayed whole-AMD movements may not reconcile exactly to balances; record any difference, inspect available finer precision, and never silently replace a confirmed portal balance with a reconstructed figure. Label estimates based on unposted declarations or changing balances as provisional, with assumptions visible.

Verify receiving-account numbers against current portal information or official sources before presenting payment details. Distinguish ordinary unified, administrative-act unified, mandatory stamp-contribution, and other earmarked accounts. Never select an account just from a tax's English nickname or a donation page. Keep the payer's own TIN separate from recipient identifiers; do not guess beneficiary TIN, IBAN, SWIFT, or bank-specific fields.

Reviewing balances does not authorize creating, signing, sending, or retrying a payment order; invoking early settlement; requesting a refund; or transferring credits between accounts. If payment is requested later, prepare verified details within that request and apply the tool's required user handoff at execution.

## Suggested payment actions

Every balance review should finish with concrete suggested actions, rather than only a list of balances and account numbers. Lead with the additional money the user needs to send and its destination.

- Group obligations by verified receiving account. For each account calculate `additional funding = max(0, unpaid obligations + accepted but unposted obligations - eligible available credit)`. Match declaration references so an obligation is counted only once. Treat already-settled amounts as history, and apply shared credit once across the account's obligations, not once per tax or quarter. Do not net stamp, administrative, or other restricted credits against ordinary tax.
- Prioritize overdue obligations, then upcoming deadlines. For multiple taxes using the same account, suggest one combined funding amount and explain what it is intended to cover; do not promise a particular allocation order without verifying the applicable rules.
- Present a compact action table: **suggested action / amount in AMD / receiving account and purpose / deadline / status**. Use clear wording such as “Send X AMD to account Y for Z” when the amount and destination are verified. Mark an unposted declaration or uncertain credit as **provisional**, and name the check that would make the recommendation final. If an essential amount or account is unknown, use **verify before paying** and identify the missing detail instead of guessing.
- Show the calculation behind each funding amount, the verified payer name/TIN where needed, and official account-source links. Distinguish the receiving account number from the user's own bank account. Do not add an arbitrary buffer or silently round away an amount due; state any necessary payment-unit rounding separately.
- Where eligible credit fully covers known obligations, explicitly say **no additional transfer is needed for those obligations**, while identifying any remaining allocation/settlement check. Where there is no recorded payable amount, do not suggest a transfer merely because the account exists or the user has a tax-specific overpayment. Keep unassessed annual obligations as a separate review action.
- If a relevant payment is already processing or bank-paid but not yet credited, suggest checking that payment's receipt and treasury posting before another transfer. Do not count it as available credit prematurely or recommend duplicating it.

Payment suggestions are recommendations for the user; presenting them does not execute a transaction. Refresh the balances and payee details for every new review.

## Result

Lead with the suggested payment actions, then give the review date/cutoff, recorded overdue debt, upcoming declared amounts and deadlines, eligible credits, and supporting calculations. Explain relevant tax types plainly and identify unassessed annual obligations needing a separate applicability review. Save useful statement/history evidence outside the public repository with restricted permissions; omit authentication secrets and unnecessary personal bank details.

After an eventual payment, distinguish order status, bank execution, treasury credit, and liability allocation. A signed or sent order does not establish that debt was paid. Reconcile the refreshed statement and unified-account history before reporting settlement.
