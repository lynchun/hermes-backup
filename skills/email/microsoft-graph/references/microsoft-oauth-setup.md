# Microsoft Graph Setup Log — 12 May 2026

## App Registration (Personal Hotmail via Work Tenant)

The app was created under `stewardscapital.com` (work tenant) but needs to access `lynchun@hotmail.com` (personal account).

### Key Debugging Steps That Were Needed

1. **`signInAudience` must be `"AzureADandPersonalMicrosoftAccount"`**
   - Setting this via the Authentication UI failed with `api.requestedAccessTokenVersion is invalid`
   - Fixed via Manifest: change `"signInAudience": "AzureADMyOrg"` → `"AzureADandPersonalMicrosoftAccount"`

2. **`accessTokenAcceptedVersion` must be `2`** (not null)
   - Setting `signInAudience` to multi-tenant triggers this requirement
   - Fixed via Manifest: change `"accessTokenAcceptedVersion": null` → `2`

3. **`allowPublicClient` must be `true`** (not null)
   - Required for device code flow
   - Without this, device code endpoint returns HTTP 400

4. **Device code flow works, auth code redirect flow doesn't**
   - Redirect with SPA redirect type returned PKCE error (`AADSTS9002325`)
   - Fixed by changing redirect type from `Spa` to `Web`
   - But device code flow is simpler and more reliable

5. **Authority URL / tenant issue**
   - Using tenant-specific URL (`/b6a50686-.../`) with personal Hotmail failed
   - Using `/common/` authority fixed it
   - Device code flow uses `/common/` automatically

6. **Permissions list:** Mail.Read, Mail.Send, Mail.ReadWrite, offline_access, User.Read
   - Mail.ReadWrite is required to delete messages
   - Adding new permissions requires re-authorization via device code flow

### Commands
```python
# Device code request — use form-encoded, NOT JSON
data = urllib.parse.urlencode({
    'client_id': CLIENT_ID,
    'scope': 'https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.Send offline_access'
}).encode()
req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/devicecode',
                              data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
```

### Token Storage
- Saved at `~/.hermes/microsoft_token.json`
- Includes access_token, refresh_token, scope, expiry
- Token refresh is automatic if `offline_access` scope was granted
