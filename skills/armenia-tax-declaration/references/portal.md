# Turnover declaration portal observations

Observed on 2026-10-04 using portal version 3.70.0. These are tested UI hints for form 286, not taxpayer-specific eligibility guidance. Reinspect the visible controls and applicable current form help. Do not infer an activity, income category, rate or exemption from these observations.

## Navigation and duplicate checks

| Purpose | Armenian label | Observed route |
|---|---|---|
| Form catalog | Inspect the current catalog label | `/pages/declarationForms.jsf?pId=2&tId=1` |
| Unfinished drafts | Անավարտ հաշվետվություններ | `/pages/savedForms.jsf?pId=2&tId=2` |
| Completed reports | Լրացված հաշվետվություններ | `/pages/submittedForms.jsf?pId=2&tId=3` |
| Filed reports | Հանձնված հաշվետվություններ | `/pages/archiveForms.jsf?pId=2&fetchData=true&tId=4` |

Check the filed archive first for the exact form, year and quarter, then completed and unfinished reports. **Վավեր** means valid; inspect the current status and exact period. The completed list alone is not proof of filing. A successfully filed report can also leave a retained copy in unfinished reports, which must not be submitted again.

Form 286 used code `wc` and the observed catalog link `/pages/formWC.jsf:docCode=wc?pId=2`. The catalog showed this form effective from 2025-01-01. Select the form currently applicable to the requested period instead of navigating to this historical hint without checking.

## Tested inputs and persisted draft

- Year: `mainForm:f_taxYear`; use the currently displayed options.
- Quarter: `mainForm:f_filePeriod`; observed values I=21, II=22, III=23, IV=24.
- The period-change modal warned that entries would not be preserved, with **Այո / Ոչ** controls. Resolve it before entering amounts.
- Row 19 income: `mainForm:f_19_a`; calculated tax `mainForm:f_19_g` was readonly. Row 19 was the tested category, not a recommended category for every taxpayer.
- Row 22 totals: `mainForm:f_22_a`, `mainForm:f_22_g`, readonly. Row 27 total income: `mainForm:f_27`, readonly.
- Activity entry was split across seven fields: `f_section`, `f_segment1`, `f_segment2`, `f_group`, `f_class`, `f_subClass`, `f_specWeight`, with prefix `mainForm:activityTypes:0:` for the first observed row. Fill verified activity codes and shares; do not copy another taxpayer's values.
- Temporary save: **Հիշել Ժամանակավորապես**, ID `mainForm:saveForm`.
- Saved draft edit: `mainForm:formsTable:<row>:editLink`. Derive the row from the actual year/quarter rather than assuming the first row.

The tested UI initially showed zero calculated totals after income entry. Saving and reopening the draft produced the calculated values. Verify persisted income, tax, totals, period, activity codes and shares; do not manually write readonly calculated fields or treat an in-memory value as a saved draft.

[Form help](https://file-online.taxservice.am/help/formWCHelp.html) required amounts in AMD without luma and described the displayed formulas. Verify the current form's rounding and category rules before converting exact audit amounts into whole-dram inputs. Previous filings are evidence of a past treatment, not authority for current legal eligibility.

## Signing, submission and recovery

1. **Գրանցել**, ID `mainForm:generatePDF`, validated and registered the draft as a completed unsigned report and redirected to completed reports. Registration was distinct from filing. Before resuming, inspect whether the exact report is unsigned, signed, already submitted or accepted.
2. The Mobile ID signing control was an image link within `mainForm:formsTable`: `../images/mid.png`, tooltip **Բջջային էլեկտրոնային ստորագրություն**. It opened **Հաշվետվության ստորագրում**, with phone input `signPhoneNumber` and **Հաստատել / Փակել**. Inspect the current provider and use the user's private Mobile ID details; the observed default is not a universal provider choice.
3. Finish a concrete reviewed declaration before a binding action. Immediately before signing/submission, follow the current browser tool's action-time confirmation requirements for the exact taxpayer, period, income and tax. A skill installation or a draft request does not authorize filing. After authorization, signing displayed **Խնդրում ենք սպասել...**. Keep any phone approval with the user; never request a PIN or duplicate a pending challenge.
4. Successful signing showed `../images/image004.gif` with the taxpayer's name, disabled Mobile ID (`mid_disabled.png`), and enabled `../images/send.gif`, tooltip **Պատրաստ է ուղարկման:**. Inspect the exact report row before using its send control. If signing was interrupted, reuse a matching signed report rather than signing again.
5. Send asked whether to retain a copy in unfinished reports: **Ցանկանում՞ եք պահպանել փաստաթղթի կրկնօրինակը...**. **Այո** retained a copy and submitted in the tested flow. Retention is optional; it is not a filing requirement. Verify **Հաշվետվությունը հաջողությամբ ուղարկվեց:** and then archive acceptance, rather than inferring success from clicking.
6. A subsequent question offered early liability settlement or debit return to the unified account. This is separate from filing. Without an authorized financial request, choose **Ոչ**. Apply the current browser tool's required user handoff to consequential financial execution.
7. In **Հանձնված հաշվետվություններ**, verify the exact year/quarter, **Վավեր** and current **Այո**. Retrieve the signed report and receipt using their actual visible links. The observed link shapes were `/downloadPdf?dln=<observed-reference>&docCode=wc&type=signed_decl` and `/downloadPdf?dln=<observed-reference>&type=receipt_decl`; derive the reference from the current report, never reuse a prior filing's identifier. Compare taxpayer identity, period, amounts, registration/electronic references and filing time across the receipt and signed report.

If submission outcome is unknown, inspect the completed report and archive before retrying. Stop attempts once acceptance is established. A failed document download requires document retrieval, not another submission.

## Preview and download recovery

Filed PDF and receipt image links sometimes had empty accessible names; inspect their visible href and image tooltip. Normal clicks downloaded successfully even when download-event waiting or `downloadMedia` timed out. Check whether the expected local file exists and inspect its contents before retrying a download.

The unsigned completed-report preview (`image002.gif`, tooltip **Բացել հաշվետվությունը:**) produced Chrome `ERR_BLOCKED_BY_CLIENT`. Do not bypass browser security or keep repeating it. Back showed a form-resubmission page; avoid replaying registration. Normal navigation to the previously observed completed-reports GET route restored the list without registering another report. Filed-archive GET download links subsequently worked.

The filing and payment deadlines are separate facts to verify for the requested period using current SRC guidance and [ARLIS Tax Code](https://www.arlis.am/hy/acts/201478/latest), including Articles 261–262. Filing acceptance alone is not proof of payment.
