# Mobile ID portal observations

Observed on 2026-10-04 using portal version 3.70.0. These are navigation and control hints, not a saved account profile or a guarantee that the current page is identical. Obtain account identifiers from the user's private profile or the current request.

## Entry and account verification

- Portal: https://file-online.taxservice.am/. The observed unauthenticated route was `/pages/loginPage.jsf`; the successful landing route was `/pages/welcome.jsf`.
- An existing session may be reusable. Inspect the current page before navigating or starting a challenge. In **Իմ Մասին** (About me), match the username and **ՀՎՀՀ** against the expected private profile; match the displayed name when supplied. A redirect alone does not establish the correct taxpayer.
- A non-binding informational notice can have a **Շարունակել** (Continue) control. Inspect the notice before dismissing it; do not accept an unrelated binding agreement as part of login.

## Tested controls

| Label or purpose | Observed control |
|---|---|
| Օգտվողի անուն — username | Input `userName` |
| ՀՎՀՀ — taxpayer number | Input `tin` |
| Mobile ID mode | Image `img[src="../images/mid.jpg"]` |
| Mobile ID phone | Input `phone` |
| «ԵՍԵՄ» հարթակ — ESEM provider | Radio `mts` |
| «ՆԻԿԻՏԱ ՄՈԲԱՅԼ» — alternative provider | Radio `team` |
| Մուտք — login, in the observed ESEM mode | Button `mainForm:mtsLoginBtn` |

The small mID image was not reliably represented in the accessibility tree. Confirm it in the current screenshot or visible DOM before clicking. Enabling Mobile ID enabled the phone/provider controls and removed the password/CAPTCHA requirement in the tested path.

The tested phone field required the literal format `+(374)xxxxxxxx`, with eight national digits. Its initial country prefix was part of the input value, not a separate selector. Use the user's own phone; the `x` characters are placeholders. Recheck current formatting instructions if the page changes.

Inspect the current provider choices and use the provider supported by the user's Mobile ID arrangement. ESEM was tested; the alternative provider was not. Do not assume ESEM is correct for every user or switch providers merely to retry a failed challenge.

## Phone challenge and recovery

The tested ESEM login redirected to the visible origin `https://yesem.am:8643`, on an `/idp/yesem/authn/mobile-id/check` path. It displayed **Log in with your mobile phone** and **Please unlock your mobile phone and confirm the login**. Navigate through the portal's current flow; do not construct or save authentication redirect URLs or their query tokens.

Keep the challenge page available while the user approves on their phone, using the current browser tool's handoff capability where available. The user performs PIN entry on the phone. Do not request the PIN, launch another challenge while one is pending, or store authentication secrets.

After approval, inspect the actual return page and verify the taxpayer identity. On failure or expiry, inspect the displayed error and arrange a fresh attempt only after the existing challenge is no longer pending. If password/CAPTCHA controls remain, first check whether Mobile ID mode was enabled; follow the browser tool's current requirements for any genuinely required CAPTCHA.

Login does not authorize declarations, signing, filing, payments, refunds, identity enrollment, credential changes or access grants. Preserve a successfully authenticated tab for the next authorized task.
