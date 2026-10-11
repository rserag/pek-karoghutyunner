---
name: armenia-tax-invoices
description: Prepare, verify, or issue Armenian service account certificates (Հաշիվ վավերագիր) in Chrome using prior invoices. Use for monthly invoices and missing recent periods; preserve established fields and update verified dates and amounts. Tax returns, income extraction, and payments are separate workflows.
---

# Armenian monthly service invoices

Use Chrome and the taxpayer's established service-invoice pattern. Read [portal.md](references/portal.md) for navigation, field controls, and issuance states. Read [amounts-and-dates.md](references/amounts-and-dates.md) when deriving an amount or resolving a date. If this installed copy has a private `references/account-pattern.md`, read it for account-specific details; that file is not part of the public package.

## Establish the targets and check existing documents

1. Verify the taxpayer identity in the reporting portal, then open `Հաշվարկային փաստաթղթեր` → `Հաշիվ վավերագրեր`. Reuse the correct invoice-portal tab. Restore login if needed; an available `armenia-tax-login` skill can help.
2. Identify the customer and requested service periods. For “the last one or two months,” first check the recent gaps. Creation, issue, service, and payment dates can refer to different months; match actual coverage before deciding a month is missing. Do not expand the request into an audit of every old invoice.
3. Search issued documents, drafts, and signing history, including other users' documents where the portal supports it. Use search windows no longer than six months and record their coverage privately. Inspect cancelled/invalid documents when they affect a possible match.
4. Retrieve an already-issued matching invoice. Reuse a suitable matching draft after inspecting it; leave unrelated drafts alone. Pending recipient confirmation alone does not make an issued invoice missing.

## Reuse the established pattern

Open the relevant prior **services/work account certificate** and record its fields. If no matching document exists, use `Կրկնօրինակել` when available, or create the same document type from the inspected template. Copying creates a draft; do not edit the issued original.

Preserve the customer, no-TIN/natural-person flags, description, unit, quantity, tax treatment, and optional blanks. Change only verified period-specific dates and amounts. Do not add contract details, month labels, extra prose, or banking fields merely to improve the invoice. A foreign customer does not by itself authorize changing the established tax treatment.

Use the reviewed AMD amount for the target period. Do not assume an unchanged monthly fee or copy the old total. With quantity one, the unit price and total must reconcile to that amount; otherwise check quantity × price and the portal calculation. Invoice serial numbers are assigned by the portal, not invented or entered as a replacement for the monetary amount.

If the amount or service date is unresolved, preserve the template and completed checks, explain the specific missing input, and continue work that does not depend on it. Receipt-date arithmetic and tax-return calculations are separate from deciding an invoice's service date and amount.

## Save and verify

Save with `ՊԱՀՊԱՆԵԼ`, reopen the saved draft, and verify the persisted customer, dates, description, quantity, price, tax treatment, and total against the intended changes. A draft-only request ends with a saved unsigned draft and private evidence of its identity and contents.

Issue/sign only when the user has requested issuance of these invoices. Skill creation, testing, or publication does not authorize issuing test invoices. Follow the browser tool's current confirmation/signing requirements; the user enters Mobile ID PINs on their device.

After signing, verify the issued serial, actual issue timestamp, service date, amount, and seller-signature result in issued documents and signing history. If the account's established, user-confirmed foreign-customer workflow ends at seller issuance, an issued seller-signed invoice awaiting buyer confirmation is complete for that workflow. Do not chase the buyer's signature or treat it as a failed issuance. This is an account-specific convention, not a rule for every foreign customer.

If signing is interrupted or the result is unknown, inspect issued documents and signing history before retrying. A buyer who has not confirmed, or a failed download, is not a reason to issue another copy. If status remains ambiguous, retain the page and evidence and resolve it without creating a duplicate.

Report each target as already issued, saved draft, newly issued, or unresolved, with its verified date, amount, and document identity where available. Corrections, cancellations, return amendments, payments, schedules, and customer messages require their own requested scope.
