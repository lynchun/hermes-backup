---
name: facebook-graph-pages-api
description: Set up Meta app + Graph API Explorer to obtain Facebook Page access tokens and test page read/post permissions.
---

# Facebook Graph API for Page Management

Use this when a user needs to manage a Facebook Page via Graph API (read engagement, post content, fetch page token), especially from Graph API Explorer.

## Trigger conditions
- User has a Meta app but cannot see `pages_*` permissions.
- Graph API Explorer only shows `user_payment_tokens` or non-Page scopes.
- User needs a Page Access Token for testing.

## Core workflow
1. Confirm current Explorer state first (no guessing)
   - Selected app in `Meta App` dropdown.
   - Token type in `User or Page` dropdown.
   - Currently visible permissions.
   - Whether a token is already generated.

2. Generate a user token in Explorer
   - Click `Generate Access Token`.
   - Set `User or Page` to `User Token`.
   - Attempt to add: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts` (and often `pages_manage_metadata`).

3. If Page permissions are missing, check app use-case configuration
   - Open app dashboard > `Use cases`.
   - Ensure a Pages-specific use case is selected (e.g. `Manage everything on your Page` / Pages API).
   - If app only offers Ads-oriented use cases or Explorer only exposes `user_payment_tokens`, the app template is likely wrong for Pages.

4. If Explorer shows `No configurations available`, create a Business Login configuration
   - App dashboard > `Facebook Login for Business` > `Configurations` > `Create configuration`.
   - Choose `User access token` for personal-account testing.
   - Save even if only `pages_show_list` + `business_management` are available at this stage.
   - Return to Explorer and select that configuration in the `Configurations` tab.

5. If template/use-case mix is wrong, create a new app with the correct primary use case
   - During app creation, select the Pages use case (`Manage everything on your Page` / Pages API) first.
   - Complete creation, then return to Explorer and select the new app.

6. Obtain page token
   - In Explorer: `User or Page` -> `Get User Access Token` and generate consent flow.
   - Then `User or Page` -> `Get Page Access Token` and choose the page.

7. Verify with live calls
   - `GET /me/accounts` (should list page entries including `id`, `access_token`, and `tasks`).
   - If available tasks include `CREATE_CONTENT`/`MANAGE`, copy that page `access_token` and use it directly for posting tests.
   - `GET /{page-id}?fields=id,name`
   - `POST /{page-id}/feed` with `message=...` (test post).

## Pitfalls
- `user_payment_tokens` as the only addable permission in Explorer usually indicates wrong app/use-case class for Page APIs.
- `No configurations available` in Explorer means the app is missing a Business Login configuration; create one under `Facebook Login for Business` > `Configurations`.
- `Configurations` tab greyed out in Explorer often means no config exists yet or wrong app is selected in `Meta App`.
- In newer Business Login app templates, the classic `Review` / `Permissions and features` menu may not be present. Do not send users to non-existent menus; work from `Facebook Login for Business` and Explorer.
- Business Login configuration may expose only `pages_show_list` + `business_management`. This is normal in some templates; do not loop trying to force extra scopes there.
- If `/me/accounts` returns page entries with `tasks` containing `CREATE_CONTENT`/`MANAGE`, proceed by using that returned page `access_token` for posting tests.
- `GraphMethodException` code `100`, subcode `33` on `me/accounts` can be caused by malformed path input (leading space or wrong edge text). Retype endpoint exactly `me/accounts` (or choose `accounts` from edge autocomplete).
- If `Add more use cases` only shows unrelated options (e.g., fundraisers under `Others`), do not keep patching that app; start a fresh app with `Manage everything on your Page` as the primary use case.
- Different app IDs/names across tabs/screens can cause false debugging trails; always confirm active app ID and app name at each step.

## User-facing execution style
- Drive from the user’s actual UI/screenshots, one click sequence at a time.
- Ask for the exact visible options before recommending the next click.
- Keep instructions short and concrete while troubleshooting UI drift in Meta dashboards.
- Avoid circular guidance: after each step, define a pass/fail checkpoint and the single next branch.
- If a menu/option is not visible in the screenshot, acknowledge immediately and reroute; do not repeat prior generic paths.

## References
- See `references/pages-permissions-troubleshooting.md` for UI signatures and decision tree from real troubleshooting sessions.
- See `references/business-login-template-quirks.md` for newer Business Login template behavior and the direct page-token testing path.
