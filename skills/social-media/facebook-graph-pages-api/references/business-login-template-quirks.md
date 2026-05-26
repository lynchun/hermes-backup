# Business Login template quirks (Meta Graph API Explorer)

Use this when a user created a newer "Facebook Login for Business" + "Manage everything on your Page" app and cannot find classic Page permission controls.

## Observed UI signatures
- Explorer shows only `pages_show_list` and `business_management` in permissions.
- App config wizard permission step only offers 2 options.
- Left menu may NOT include `Review` / `Permissions and features`.
- `me/accounts` can still return page records with `id`, `access_token`, and `tasks`.

## Practical success path
1. Ensure Business Login configuration exists and is selected in Explorer.
2. Generate user token.
3. Run `GET me/accounts`.
4. From a returned page object, copy `id` and `access_token`.
5. Paste page token into Explorer token field.
6. Test `POST /{page-id}/feed` with `message=...`.

## Common false blockers
- Error code `100` subcode `33` for `me/accounts` can be a malformed endpoint string (leading space). Retype endpoint exactly.
- Repeated attempts to add unavailable scopes in this template wastes time; move to direct page-token post test once tasks include `CREATE_CONTENT`/`MANAGE`.

## Decision rule
If `me/accounts` returns page `tasks` including `CREATE_CONTENT` and `MANAGE`, run posting test immediately instead of continuing permission-UI debugging.
