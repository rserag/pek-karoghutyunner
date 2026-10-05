# PEK Karoghutyunner

Six reusable Codex skills for quarterly and yearly tax work in Armenia: Mobile ID login, income reconciliation, quarterly declarations, annual returns, turnover-tax elections, and debt/payment review.

The workflows use Chrome, [Armenia's tax portal](https://file-online.taxservice.am/), and the [rate.am Central Bank archive](https://www.rate.am/hy/armenian-dram-exchange-rates/central-bank-armenia). They preserve lessons from actual portal use while keeping taxpayer identities, bank statements, and filing records private.

| Skill | Purpose | Result |
|---|---|---|
| `armenia-tax-login` | Authenticate with the user's Mobile ID and verify the taxpayer | A verified portal session |
| `armenia-tax-income` | Review business receipts and historical CBA rates; reconcile current quarterly returns for a year | An audited quarterly AMD calculation or an annual income/turnover reconciliation |
| `armenia-tax-declaration` | Check existing filings and prepare the applicable turnover-tax form | A saved draft, or an accepted filing when explicitly requested |
| `armenia-tax-annual-returns` | Check annual applicability and prepare forms 240/244 for turnover-tax individual entrepreneurs | Separate verified liability worksheets and saved drafts, or accepted filings when requested |
| `armenia-tax-turnover-election` | Check eligibility, deadline case and effective date for form 201 | A reviewed turnover-tax election draft, or accepted statement when requested |
| `armenia-tax-balances` | Reconcile liabilities, credits, treasury deposits, and accounts | Suggested amounts and destinations, with posting/allocation checks |

## Install

Use a Codex environment with skills support, Chrome, and an enabled browser-control tool. Mobile ID requires the user's own supported account and phone. PDF statements require an available PDF reader/extractor. The optional arithmetic helper needs Python 3.9+ and uses only the standard library.

Ask Codex:

```text
Use $skill-installer to install these paths from rserag/pek-karoghutyunner:
skills/armenia-tax-login
skills/armenia-tax-income
skills/armenia-tax-declaration
skills/armenia-tax-annual-returns
skills/armenia-tax-turnover-election
skills/armenia-tax-balances
```

For manual installation, copy the six folders under `skills/` into your environment's skill directory without overwriting existing personal versions. Each folder is self-contained; related skills are optional workflow aids. Current Codex documentation lists `~/.agents/skills` for user skills and `.agents/skills` for repository skills. Older or configured environments may use a different location. See the [official skills documentation](https://developers.openai.com/codex/skills).

This repository also includes a portable `plugin.json` manifest for clients that support [agent plugin bundles](https://developers.openai.com/plugins/build/plugins). Browser tooling is supplied by the host; this package adds no browser server. Publication here does not imply inclusion in a plugin directory.

## Private account context

Supply your identifiers in the conversation, or copy [profile.example.json](examples/profile.example.json) to a location **outside this repository**, such as `~/.config/armenia-tax/profile.json`. Keep the directory private (POSIX mode `700`) and the file private (`600`). Point Codex to the file in your request or set `ARMENIA_TAX_PROFILE` to its path.

The profile holds username, taxpayer number, Mobile ID phone/provider, and tax context. It must never contain PINs, OTPs, passwords, cookies, or session tokens. Prior activity codes and recognition preferences are context to verify for the reporting period, not permanent eligibility rules.

Optional registration, regime-history, suspension/resumption and social-participation records can point to private evidence for yearly work. Recheck their relevance for the requested year; a stored profile does not certify election eligibility or annual exemptions. Do not place dates of birth, annual returns or real evidence paths in contributed examples.

Keep bank statements, extracted transactions, screenshots, drafts, receipts, and reports outside this repository. The `.gitignore` adds an extra safeguard; review staged files before publishing anything.

## Use

```text
Use $armenia-tax-login to sign me in through Chrome and verify my taxpayer identity.

Use $armenia-tax-income to review my bank statement for Q1 2024.
Verify the applicable recognition, CBA rate-date, and rounding rules first.

Use $armenia-tax-declaration to prepare an unsigned draft from my finalized calculation.
Check the archive for an existing filing before creating anything.

Use $armenia-tax-income to reconcile my current accepted turnover-tax returns
and audited income for 2026. Identify missing quarters and corrections.

Use $armenia-tax-annual-returns to prepare unsigned 240 and 244 drafts for 2026.
Verify the applicable form versions and calculate each obligation separately.

Use $armenia-tax-turnover-election to check my eligibility and prepare an unsigned
form 201 statement for 2027, using the correct deadline case and effective date.

Use $armenia-tax-balances to review my debt and credits and suggest how much
additional money to send to each verified receiving account.
```

The declaration workflow uses observed form 286 controls as navigation hints. It verifies the applicable form, categories, activity codes, and rates for the taxpayer and period. It has no universal software-services rate or exemption. A draft request stops at a saved unsigned draft. Filing requires an explicit request and the browser tool's required signing/confirmation steps. Payment suggestions show amounts and receiving accounts; payment execution is a separate task.

The balances workflow distinguishes bank execution, treasury posting, and liability allocation. An accepted declaration may appear after the statement's cutoff. Available unified credit may remain unallocated. A transfer that has not appeared is checked before recommending another payment.

## Yearly workflows

The annual-returns skill focuses on turnover-tax individual entrepreneurs and accepts requests for 240, 244, or both. It checks registration, regime history, liability months, social-payment applicability and the current quarterly turnover evidence before entering amounts. Prior-year forms are examples, not reusable amounts or proof of exemption. It keeps profit-tax, social and stamp calculations independent and checks reporting-year rules against official sources.

The revised form 244 adds a stamp-fee section under [order 1437-N as amended](https://www.arlis.am/hy/acts/219232), effective July 2026. The first annual reporting period served by the revised portal form must be confirmed before preparing a return; the workflow does not silently choose a version. The profit-tax suspension exemption is verified, but equivalent social-payment treatment remains a separate unresolved check. Evidence gaps are reported before affected fields are entered.

Form 201 elects turnover-tax status for the requested year or statutory registration/resumption case. Its eligibility attestations, effective date and filing deadline are verified independently of quarterly return rates. [Official government instructions](https://hartak.am/services/2e560b1b-1bfd-4017-a180-72945fec90a0/online/) identify the form and normal annual February deadline; the skill checks the law and the applicable calendar before recommending a specific deadline. An ordinary missed election deadline cannot be repaired by inventing a later effective date.

Annual work produces evidence worksheets, drafts and acceptance documents within the requested scope. Filing still requires an explicit request and the browser tool's required confirmations; payment remains separate. The package does not schedule reminders or submit forms automatically.

## Arithmetic helpers

The helper operates on externally verified **receipt-date** inputs. It cannot represent another recognition date by changing a text label. If the applicable method differs, use a separate reviewed calculation. It neither fetches exchange rates nor decides which credits are taxable.

Try the entirely invented [synthetic example](examples/income.synthetic.json):

```sh
python3 skills/armenia-tax-income/scripts/calculate.py \
  examples/income.synthetic.json \
  --output /tmp/armenia-tax-demo/result.json \
  --html /tmp/armenia-tax-demo/report.html
```

Use a private output folder for real data. The input makes the rate-date rule, currency quote units, receipt/declaration rounding, and optional tax rate explicit. The helper rounds individual receipts to two decimal places before rounding their sum to whole dram. Aggregate-only or other unsupported rounding requires a separate verified calculation. Duplicate transaction identities are rejected. Native AMD receipts need no exchange rate. Reports separate precise conversions, rounded receipts, and whole-dram declaration input. See the [full schema and limitations](skills/armenia-tax-income/references/method.md).

The annual helper reconciles externally verified quarterly records and their current accepted filings. It does not extract receipts, decide that a quarter required no return, determine social months, or calculate a contribution. Missing quarters and audit evidence produce an incomplete result, not an assumed zero. The report preserves precise audited income separately from the sum of accepted whole-dram turnover and identifies rounding/correction differences. See the [annual schema](skills/armenia-tax-income/references/annual.md) and [synthetic annual example](examples/annual.synthetic.json).

```sh
python3 skills/armenia-tax-income/scripts/reconcile_annual.py \
  examples/annual.synthetic.json \
  --output /tmp/armenia-tax-demo/annual.json \
  --html /tmp/armenia-tax-demo/annual.html
```

## Verification and maintenance

```sh
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
```

Tests use synthetic data only. They cover dates and quarter boundaries, duplicate receipts, currencies and quote units, rounding, input validation, escaped HTML, private output permissions, and annual completeness/correction selection/reconciliation. The package check validates all six skill folders, metadata, local links, synthetic examples, and manifest. CI runs these checks on Python 3.9 and 3.12.

Quarterly portal controls were observed in October 2026 and must be checked against the live page. The annual and election references distinguish public form evidence from unverified live controls. Tax rules, deadlines, and receiving accounts must be verified from current official sources for each review. Automated checks validate the package and arithmetic; they do not certify a future portal workflow or taxpayer eligibility.

See [CONTRIBUTING.md](CONTRIBUTING.md) for privacy requirements and workflow review scenarios. Licensed under [MIT](LICENSE).
