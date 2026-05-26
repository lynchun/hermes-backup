#!/usr/bin/env python3
"""Microsoft Graph device code flow setup for Hotmail/Outlook.
Usage:
  python3 hotmail_setup.py --device-code   # Step 1: get auth code
  python3 hotmail_setup.py --poll           # Step 2: poll for token after user auth
  python3 hotmail_setup.py --check          # Step 3: verify
  python3 hotmail_setup.py --test           # List inbox messages to verify access
"""
import json, urllib.request, urllib.parse, sys, os
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser('~/.hermes'))
TOKEN_PATH = HERMES_HOME / 'microsoft_token.json'
PENDING_PATH = HERMES_HOME / 'microsoft_pending.json'
CLIENT_ID = os.environ.get('MS_CLIENT_ID', '')  # Set in .env or pass via --client-id

if not CLIENT_ID:
    print('ERROR: Set MS_CLIENT_ID env var or edit this script with your app client ID')
    sys.exit(1)

SCOPES = 'https://graph.microsoft.com/Mail.ReadWrite https://graph.microsoft.com/Mail.Send offline_access'

def device_code():
    data = urllib.parse.urlencode({'client_id': CLIENT_ID, 'scope': SCOPES}).encode()
    req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/devicecode',
                                  data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {e.read().decode()}')
        sys.exit(1)
    print(f'Go to: {resp["verification_uri"]}')
    print(f'Enter code: {resp["user_code"]}')
    PENDING_PATH.write_text(json.dumps({
        'device_code': resp['device_code'], 'interval': resp['interval'],
        'expires_in': resp['expires_in'],
    }))

def poll():
    pending = json.loads(PENDING_PATH.read_text())
    data = urllib.parse.urlencode({
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id': CLIENT_ID, 'device_code': pending['device_code'],
    }).encode()
    req = urllib.request.Request('https://login.microsoftonline.com/common/oauth2/v2.0/token',
                                  data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        if 'access_token' in resp:
            TOKEN_PATH.write_text(json.dumps(resp, indent=2))
            PENDING_PATH.unlink(missing_ok=True)
            print('OK: Authenticated!')
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        if body.get('error') == 'authorization_pending':
            sys.exit(2)  # Keep polling
        print(f'ERROR: {body}')

def check():
    if TOKEN_PATH.exists():
        print('AUTHENTICATED')
        token = json.loads(TOKEN_PATH.read_text())
        print(f'Scopes: {token.get("scope", "?")}')
    else:
        print('NOT_AUTHENTICATED')

def test():
    token = json.loads(TOKEN_PATH.read_text())
    headers = {'Authorization': f'Bearer {token["access_token"]}'}
    req = urllib.request.Request(
        'https://graph.microsoft.com/v1.0/me/messages?$top=5&$select=subject,from,receivedDateTime',
        headers=headers)
    resp = json.loads(urllib.request.urlopen(req).read())
    for msg in resp.get('value', []):
        f = msg.get('from', {}).get('emailAddress', {})
        print(f'  {f.get("address","?"):30s} | {msg.get("subject","?")[:60]}')

if __name__ == '__main__':
    cmds = {'--device-code': device_code, '--poll': poll, '--check': check, '--test': test}
    cmd = sys.argv[1] if len(sys.argv) > 1 else '--check'
    cmds.get(cmd, check)()
