# Invoice portal controls and states

Navigation and field hints were inspected on 2026-10-11 in reporting portal version 3.70.0 and invoice portal version 1.0.60. Reinspect the live page before using them. The [official invoicing user guide](https://e-invoicing.taxservice.am/resources/invoicing_user_guide.pdf) supplies the copy/save/sign transitions noted below.

## Entry and document search

`Հաշվարկային փաստաթղթեր` → `Հաշիվ վավերագրեր` opens the separate [invoice portal](https://e-invoicing.taxservice.am/). Verify the taxpayer and inspect the tab inventory before opening another copy.

| Area | Observed path |
|---|---|
| Account certificates overview | `/main/account-certifications` |
| Issued | `/issued/account-certifications` |
| Drafts | `/draft/account-certifications` |
| Invalid, cancelled, deleted | Corresponding `/invalid/`, `/cancelled/`, `/deleted/` account-certification paths |
| Signing history | `/at-signing` |
| New services/work document | `/acc-doc-services/create` |

The list defaults to a recent six-month window. A search accepts at most six months. `ՄԱՔՐԵԼ` resets the default window; it does not search all history. Open the filter, set both dates, close any calendar overlay, and activate the visible search control. Read the resulting dates and row count. The overview's recent rows are not an exhaustive archive.

Use the option to include other users' documents when available (guide pp. 125–126). Search issued, draft, and signing areas separately. Distinguish the filter's issue/creation date from the service date displayed in a document. Match customer, service coverage, amount, and retained source evidence, not just the month of issue.

## Open or copy a prior document

Double-click a row to open its details (guide p. 124); inspect the tab inventory if the original page does not change. Selecting a serial alone may only select the row. The issued-list `Կրկնօրինակել` action copies the selected document into a draft (guide pp. 118, 125). It is a mutation, not a read-only inspection.

Choose the same **services/work account certificate** as the prior invoice. Do not substitute a tax invoice or goods document. The prior invoice's customer flags and treatment are a template to preserve within the user's request, not a universal classification rule.

## Observed service-document fields

These IDs are hints for exact-ID locators after inspecting the current DOM. Several contain `/`; avoid unescaped CSS selectors or stale accessibility-node indexes.

| Field | Observed ID |
|---|---|
| On whose behalf | `/accDocServices/State/behalfOf` |
| Service/delivery date | `/accDocServices/State/deliveredAt` |
| Additional information | `/accDocServices/State/additionalInfo` |
| Contract date / number | `/accDocServices/State/dealtAt`, `/accDocServices/State/dealNo` |
| Buyer has no TIN / is a natural person | `buyerHasNoTin`, `buyerIsNatural` |
| Buyer name / address | `buyerName`, `buyerAddress` |
| First line description | `/accDocServices/Subject/name/0` |
| First line unit / quantity / unit price | `/accDocServices/Subject/unit/0`, `/accDocServices/Subject/quantity/0`, `/accDocServices/Subject/unitPrice/0` |
| First line deal type / total | `/accDocServices/Subject/dealType/0`, `/accDocServices/Subject/totalValue/0` |
| Document total | `/accDocServices/State/totalValue` |

When the template uses “buyer has no TIN,” preserve the verified buyer name, address, and flag; do not invent a TIN or mark a company as a natural person. The guide covers no-TIN buyers where permitted (pp. 167–168) and service lines (p. 173). Preserve blank optional contract, additional-information, and banking fields unless the current request requires a supported change.

## Saving and issuance

The inspected new form had `ՊԱՀՊԱՆԵԼ` and a disabled `ՍՏՈՐԱԳՐԵԼ` before saving. Save, reopen, and verify persisted fields and calculated totals before signing. Issued fields were disabled and the document displayed a serial and seller signature.

The guide describes signing as assigning a serial, adding the seller signature and signing date, registering the document, and moving it to issued documents (pp. 116–117). Recipient confirmation is a separate action (p. 136). Inspect both the issued document and signing history; list text alone does not establish whether seller signing succeeded.

For an account whose user confirms that a foreign buyer cannot sign and the agreed process ends at seller issuance, retain an issued seller-signed document even when the list awaits buyer confirmation. Store that convention in private account context rather than treating it as general legal advice.

Read-only lists, existing-document details, and an unsaved new form were inspected for this skill. Copying, draft persistence, and signing transitions are based on the official guide and still require verification during an authorized real invoice task. Synthetic tests do not certify those live transitions.

Do not change an issued original to fix a new-period invoice. Corrections/cancellations follow their own procedure under [Government Decision 1257-N](https://www.arlis.am/hy/acts/192241) and require a separate request.
