---
name: armenia-tax-login
description: Sign into Armenia's electronic tax reporting portal in Chrome using Mobile ID, or restore an expired session before tax work. Verify the taxpayer identity after authentication. Use for login, not income calculations, declaration filing, or payments.
---

# Armenia tax portal login

Use Chrome through an available browser-control tool. Follow that tool's current instructions for observation, authentication, and user handoff. Read [references/portal.md](references/portal.md) for observed Armenian labels and control hints; inspect the live page before acting.

## Account context

Use identifiers provided by the user in this session or an explicitly supplied private profile outside the public skill directory. A user may point to a JSON profile with `ARMENIA_TAX_PROFILE`; read only the fields needed for the task. Relevant fields are `identity.username`, `identity.tin`, `identity.expected_display_name`, `mobile_id.international_phone`, and `mobile_id.provider`. Ask for required missing identifiers or an ambiguous provider. Do not assume another taxpayer's account or a particular Mobile ID provider.

Never request, record, or store phone PINs, OTPs, passwords, cookies, session tokens, or authentication redirect tokens. Keep identifiers and browser evidence out of the public repository.

## Sign in

1. Inspect the existing tax portal tab in Chrome. If the authenticated page shows the expected username and taxpayer number (ՀՎՀՀ), reuse the session. Otherwise open https://file-online.taxservice.am/.
2. Enter the username in **Օգտվողի անուն** and taxpayer number in **ՀՎՀՀ**. Enable **mID** mode using the control confirmed in the current screenshot or DOM. The image may be absent from the accessibility tree.
3. Choose the user's Mobile ID provider from the live controls. Match the phone field's current formatting; its country prefix may already be part of the value. Verify the complete phone number before clicking **Մուտք**.
4. When the identity provider requests phone approval, hand control to the user and ask them to unlock their phone and approve the login. They enter any PIN on their own device. Preserve the tab while waiting; do not issue duplicate challenges.
5. After the user confirms approval, inspect the page again. Verify return to the tax portal and the expected username and ՀՎՀՀ in **Իմ Մասին**; compare the displayed name when supplied. A redirect alone does not verify the account. Stop on an identity mismatch.
6. Report successful authentication and preserve the tab for the authorized next task. A login-only request ends here.

## Recovery

- If Mobile ID controls or providers changed, inspect the live page and use the user's supported provider. Saved selectors are hints, not permission to operate unseen controls.
- If a challenge fails or expires, inspect the error and arrange one fresh attempt when the user is ready. Do not silently switch providers.
- If CAPTCHA remains, first verify that Mobile ID mode was enabled. If the live flow genuinely requires it, follow the browser tool's policy or hand it to the user.
- Normal login authorization does not authorize enrolling an identity, changing credentials, granting new access, or bypassing certificate warnings.
