# Microsoft Graph API — Setup for Hotmail/Outlook Email Access

When IMAP fails (Microsoft now requires OAuth2 for all connections), use the
Microsoft Graph API as an alternative. This reference documents the setup used
for lynchun@hotmail.com.

## Quick Setup (Device Code Flow)

The device code flow is the simplest OAuth2 flow for personal Microsoft accounts:

```python
import urllib.request, urllib.parse, json, time

CLIENT_ID = 'your-client-id'
SCOPES = 'https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.Send offline_access'

# Step 1: Get device code
data = urllib.parse.urlencode({
    'client_id': CLIENT_ID,
    'scope': SCOPES
}).encode()
req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/devicecode',
                              data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
resp = json.loads(urllib.request.urlopen(req).read())
print(f'Go to {resp["verification_uri"]} and enter code: {resp["user_code"]}')

# Step 2: Poll for token
device_code = resp['device_code']
for _ in range(60):
    data = urllib.parse.urlencode({
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id': CLIENT_ID,
        'device_code': device_code,
    }).encode()
    req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/token',
                                  data=data,
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        token = json.loads(urllib.request.urlopen(req).read())
        if 'access_token' in token:
            break  # success
    except urllib.error.HTTPError:
        time.sleep(2)  # authorization_pending — keep polling
```

## Azure App Registration Requirements

1. Create app at https://portal.azure.com (requires Azure AD tenant)
2. In the **Manifest**, set these values:
   - `signInAudience`: `"AzureADandPersonalMicrosoftAccount"` (critical — the default `AzureADMyOrg` blocks personal Microsoft accounts)
   - `allowPublicClient`: `true` (required for device code flow)
   - `accessTokenAcceptedVersion`: `2` (v2.0 tokens required for Graph API)
3. Add API permissions (all **Delegated**):
   - `Mail.Read` — read inbox/search
   - `Mail.ReadWrite` — delete/modify messages (needed for junk cleanup, moving, etc.)
   - `Mail.Send` — send emails
   - `offline_access` — token refresh without user present
4. No redirect URI needed for device code flow

## Deleting Messages (Junk Cleanup, etc.)

Requires `Mail.ReadWrite` scope. Delete a single message:

```python
req = urllib.request.Request(
    f'https://graph.microsoft.com/v1.0/me/messages/{message_id}',
    method='DELETE', headers=headers)
urllib.request.urlopen(req)  # Returns 204 on success
```

To empty a folder (e.g. JunkEmail), fetch all IDs then delete individually:

```python
# Fetch IDs
url = 'https://graph.microsoft.com/v1.0/me/mailFolders/JunkEmail/messages?$top=200&$select=id'
req.add_header('ConsistencyLevel', 'eventual')
resp = json.loads(urllib.request.urlopen(req).read())
all_ids = [m['id'] for m in resp.get('value', [])]
# Delete each
for msg_id in all_ids:
    req = urllib.request.Request(
        f'https://graph.microsoft.com/v1.0/me/messages/{msg_id}',
        method='DELETE', headers=headers)
    urllib.request.urlopen(req)
```

Note: 403 on delete means `Mail.ReadWrite` is missing from scopes. The token must be re-authenticated after adding the scope (old token doesn't upgrade automatically).

## Reading Emails

```python
headers = {'Authorization': f'Bearer {access_token}'}
req = urllib.request.Request('https://graph.microsoft.com/v1.0/me/messages?$top=10&$select=subject,from,receivedDateTime',
                              headers=headers)
data = json.loads(urllib.request.urlopen(req).read())
for msg in data.get('value', []):
    sender = msg['from']['emailAddress']['address']
    subject = msg['subject']
    print(f'{sender}: {subject}')
```

## Sending Emails

```python
email_data = json.dumps({
    'message': {
        'subject': 'Subject here',
        'body': {'contentType': 'Text', 'content': 'Body text'},
        'toRecipients': [{'emailAddress': {'address': 'recipient@example.com'}}]
    }
}).encode()
req = urllib.request.Request('https://graph.microsoft.com/v1.0/me/sendMail',
                              data=email_data,
                              headers={'Authorization': f'Bearer {access_token}',
                                       'Content-Type': 'application/json'})
urllib.request.urlopen(req)
```

## Token Refresh

The device code flow returns a `refresh_token`. Use it to get new tokens:

```python
data = urllib.parse.urlencode({
    'client_id': CLIENT_ID,
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token',
    'scope': SCOPES,
    'client_secret': CLIENT_SECRET,  # only if app has a client secret
}).encode()
req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/token',
                              data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
token = json.loads(urllib.request.urlopen(req).read())
```

## Limitations

- **10,000 requests per day** per app (sufficient for personal email)
- Device code expires after 15 minutes if user doesn't authenticate
- No push/notification support (polling only)
- The `common` endpoint works for both personal and work/school accounts
- Sending mail requires `Mail.Send` scope AND mailbox capacity

## Troubleshooting

- `AADSTS50020` — account from one provider doesn't exist in the app's tenant. Use `/common` authority.
- `AADSTS900144` — request body format wrong (use `x-www-form-urlencoded`, not JSON, for device code endpoint)
- `AADSTS70016` — user hasn't entered the device code yet
- `allowPublicClient: null` must be changed to `true` in the manifest for device code flow
- `accessTokenAcceptedVersion: null` must be changed to `2` for v2.0 tokens
