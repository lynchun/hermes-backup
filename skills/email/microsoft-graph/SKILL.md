---
name: microsoft-graph
description: "Set up Microsoft Graph API access via Azure app registration and OAuth device code flow. Covers creating an Azure AD app, configuring API permissions (Mail.Read, Mail.Send, Mail.ReadWrite, offline_access), using device code flow for personal/work accounts, and reading/sending email via Graph API."
version: 1.0.0
author: Epictetus
metadata:
  hermes:
    tags: [microsoft, graph, oauth, email, azure, hotmail, outlook]
---

# Microsoft Graph API Setup

Set up email access for Hotmail/Outlook accounts via Microsoft Graph API. This is the recommended approach over IMAP — Microsoft has fully deprecated password-based IMAP/SMTP auth, and even app passwords are rejected.

## Azure App Registration

1. Go to **https://portal.azure.com** — sign in with a Microsoft account that has Azure AD access (work/school account or personal with free trial)
2. Search for **"App registrations"** → **"New registration"**
3. Name: `Hermes Agent` (or any name)
4. **Supported account types:** Choose based on the target mailbox:
   - For personal Hotmail/Outlook: "**Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)**"
   - For work/school only: "Single tenant"
5. Click **Register**

### Required Manifest Changes

After registration, go to **"Manifest"** in the left menu and set:
```json
"signInAudience": "AzureADandPersonalMicrosoftAccount",
"accessTokenAcceptedVersion": 2,
"allowPublicClient": true
```
(If `signInAudience` was `"AzureADMyOrg"`, changing it in the UI may fail with `api.requestedAccessTokenVersion` error — fix via Manifest instead.)

### API Permissions

Go to **"API permissions"** → **"Add a permission"** → **Microsoft Graph** → **Delegated permissions**. Add:
- `Mail.Read` — read emails
- `Mail.Send` — send emails
- `offline_access` — token refresh (keeps access alive)
- `Mail.ReadWrite` — only if you need to delete/modify messages (e.g. clearing junk)
- `User.Read` — added automatically (sign-in profile)

Do NOT use Application permissions (they're for server-to-server, not for reading personal mailboxes).

### Client Secret (if using auth code flow)

Go to **"Certificates & secrets"** → **"New client secret"**:
- Description: `Hermes Agent`
- Expires: `24 months`
- Copy the **Value** immediately — shown once only

The client secret is required for the auth code redirect flow but NOT for the device code flow (which uses `allowPublicClient: true` instead).

## Auth Flows

### Device Code Flow (Recommended — works with any account, no redirect URI needed)

This is the simplest approach for personal Microsoft accounts. No client secret needed (only requires `allowPublicClient: true` in manifest).

**Step 1 — Get device code:**
```python
data = urllib.parse.urlencode({
    'client_id': CLIENT_ID,
    'scope': 'https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.Send offline_access'
}).encode()
req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/devicecode',
                              data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
resp = json.loads(urllib.request.urlopen(req).read())
print(f"Code: {resp['user_code']}")
print(f"URL: {resp['verification_uri']}")
```

**Step 2 — User authenticates:**
- User goes to `https://login.microsoft.com/device`
- Enters the code shown
- Signs in with their Microsoft account
- Accepts the permissions

**Step 3 — Poll for token (keep checking until user completes):**
```python
data = urllib.parse.urlencode({
    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
    'client_id': CLIENT_ID,
    'device_code': pending['device_code'],
}).encode()
req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/token',
                              data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
resp = json.loads(urllib.request.urlopen(req).read())
# If 'access_token' in resp → authenticated
# If error == 'authorization_pending' → keep polling
```

**Step 4 — Save token** to `~/.hermes/microsoft_token.json`

### Authorization Code Flow (Alternative — requires redirect URI)

Use `http://localhost:1` as the redirect URI and register it as type `Web` in the manifest. This flow needs the client secret from step above. Same process as Google Workspace OAuth.

## IMAP Note

Microsoft IMAP (`outlook.office365.com:993`) now requires OAuth2/XOAUTH2. Standard password and app password auth are fully deprecated. If IMAP is essential, you need to implement XOAUTH2 SASL authentication. For most use cases, the Graph API is simpler and more reliable.

## Reading Email (Graph API)

```python
token = json.loads(open('~/.hermes/microsoft_token.json').read())
headers = {'Authorization': f'Bearer {token["access_token"]}'}

# List inbox
req = urllib.request.Request(
    'https://graph.microsoft.com/v1.0/me/messages?$top=10&$select=subject,from,receivedDateTime',
    headers=headers)
resp = json.loads(urllib.request.urlopen(req).read())

# List junk folder
req = urllib.request.Request(
    'https://graph.microsoft.com/v1.0/me/mailFolders/JunkEmail/messages?$top=10&$select=subject,from',
    headers=headers)

# Delete a message (requires Mail.ReadWrite)
req = urllib.request.Request(
    f'https://graph.microsoft.com/v1.0/me/messages/{msg_id}',
    method='DELETE', headers=headers)
```

## Trigger

Load this skill when the user asks to:
- Set up Hotmail/Outlook email access
- Create an Azure app registration for OAuth
- Integrate a Microsoft email account
- Troubleshoot Microsoft Graph API access
- Configure email sending/reading for a Microsoft account

## Pitfalls

- **App password no longer works** for IMAP — confirmed May 2026. Microsoft has deprecated password-based IMAP entirely. Use Graph API or OAuth2-only IMAP.
- **Device code flow needs `allowPublicClient: true`** in the manifest. Without it, the device code endpoint returns a 400 error.
- **SignInAudience mismatch:** If the app was created under a work tenant (e.g. `stewardscapital.com`) but needs to access a personal Hotmail account, the user must change `signInAudience` to `"AzureADandPersonalMicrosoftAccount"` in the manifest AND use `/common/` as the authority (not the tenant-specific auth endpoint). If it still fails, use the device code flow (it routes through `/common/` automatically).
- **Tenant-specific auth URL** will fail with personal accounts if the app's home tenant is different. Use `/common/` authority or device code flow.
- **Batch delete** via Graph API has quirks — single delete works reliably.
- **Token refresh** is handled automatically if `offline_access` scope is granted. The token file includes a `refresh_token`.
- **Token file location:** `~/.hermes/microsoft_token.json`
- **Mail.ReadWrite is required to delete messages**, not just Mail.Read.
