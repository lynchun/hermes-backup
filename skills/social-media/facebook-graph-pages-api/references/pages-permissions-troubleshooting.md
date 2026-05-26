# Pages permissions missing in Graph API Explorer

## Symptom signatures
- `Add a Permission` only shows `user_payment_tokens`.
- `Get Page Access Token` appears in dropdown, but no pages scopes can be added to user token.
- `Use cases` panel for current app only offers Ads-oriented options.
- Explorer shows `No configurations available` when selecting `Get User Access Token`.
- Explorer `Configurations` tab is greyed out.

## Diagnosis
This usually means the app was created with an incompatible use-case/template for Pages API scopes.

## Corrective path
1. Open app `Use cases`.
2. If no Pages use case exists for that app, create a new app.
3. In new app creation flow, choose `Manage everything on your Page` (Pages API) at use-case selection.
4. In the same app, open `Facebook Login for Business` > `Configurations` > `Create configuration`.
5. Choose `User access token` for personal-account testing and save the configuration (even if only `pages_show_list` and `business_management` are listed).
6. In Graph API Explorer, select the same app, open `Configurations` tab, and select the newly created configuration.
7. Generate user token and then attempt to add/request:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - optional/common: `pages_manage_metadata`
8. Generate/select Page Access Token from dropdown.

## Verification calls
- `GET /me/accounts`
- `GET /{page-id}?fields=id,name`
- `POST /{page-id}/feed` with test `message`

## Operator notes
- Always confirm active app ID because users often have multiple app tabs.
- Ask for screenshots before each branching step; Meta UI labels drift frequently.
