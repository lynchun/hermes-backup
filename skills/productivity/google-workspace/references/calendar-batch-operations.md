# Calendar Batch Operations (Python, no CLI)

When `google_api.py` does not work (Python 3.9 incompatibility on macOS) and you need to create multiple calendar events in one session, use the Google API client library directly.

## Prerequisites

- Token at `~/.hermes/google_token.json`
- Google Calendar API enabled in GCP Console (`https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/overview?project=256812641060`)
- Python packages: `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`

## Known GCP Project

Lyndon's GCP project with Google OAuth is project ID `256812641060`. Calendar API may not be enabled by default — if you get `HttpError 403: Access Not Configured`, send the user the enable URL.

## Pattern for flight events

Create TWO events per leg (departure at origin timezone, arrival at destination timezone) so the calendar shows correct local time at each end.

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(
    '/Users/lyndonarthurson/.hermes/google_token.json',
    ['https://www.googleapis.com/auth/calendar']
)
service = build('calendar', 'v3', credentials=creds)

events = [
    {
        'summary': 'CX138 Depart SYD',
        'description': 'Flight CX138 SYD -> HKG\nTerminal 1\nBooking ref: FKRQST',
        'start': {'dateTime': '2026-06-10T21:55:00+10:00', 'timeZone': 'Australia/Sydney'},
        'end': {'dateTime': '2026-06-10T21:55:00+10:00', 'timeZone': 'Australia/Sydney'},
    },
    {
        'summary': 'CX138 Arrive HKG',
        'description': 'Flight CX138 SYD -> HKG\nTerminal 1\nBooking ref: FKRQST',
        'start': {'dateTime': '2026-06-11T05:10:00+08:00', 'timeZone': 'Asia/Hong_Kong'},
        'end': {'dateTime': '2026-06-11T05:10:00+08:00', 'timeZone': 'Asia/Hong_Kong'},
    },
]

for event in events:
    result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created: {result.get('htmlLink')}")
```

## User's calendar config

- **Calendar**: `lyndonjarthurson@gmail.com` (primary)
- **OAuth token path**: `~/.hermes/google_token.json`
- **GCP project ID**: `256812641060`
