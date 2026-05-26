# HTML → Playwright PDF → Drive Upload/Replace

A repeatable pipeline for generating PDFs from HTML and replacing existing Drive files. Used for health dashboard updates, clinical summaries, and any report that needs to live on Google Drive as a PDF.

## Prerequisites

- Playwright (`pip3 install playwright`) with Chromium installed (`playwright install chromium`)
- Google OAuth token at `~/.hermes/google_token.json`
- `google-api-python-client` and `google-auth` (`pip3 install google-api-python-client google-auth`)

## Python 3.9 on macOS

The bundled `google_api.py` script uses `str | None` syntax (Python 3.10+). **Do NOT use it on macOS.** Instead, call the Google API directly via Python:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(
    '/Users/lyndonarthurson/.hermes/google_token.json'
)
drive = build('drive', 'v3', credentials=creds)
```

## Full Pipeline

```python
from playwright.sync_api import sync_playwright
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

HTML_PATH = '/path/to/source.html'
PDF_PATH = '/tmp/output.pdf'
DRIVE_FILE_ID = 'FILE_ID_TO_REPLACE'

# Step 1: HTML → PDF
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file://' + HTML_PATH)
    page.wait_for_load_state('networkidle')
    page.pdf(
        path=PDF_PATH,
        format='A4',
        print_background=True,
        margin={'top': '15mm', 'bottom': '15mm', 'left': '15mm', 'right': '15mm'}
    )
    browser.close()

# Step 2: Upload to Drive (replace existing file)
creds = Credentials.from_authorized_user_file(
    '/Users/lyndonarthurson/.hermes/google_token.json'
)
drive = build('drive', 'v3', credentials=creds)

media = MediaFileUpload(PDF_PATH, mimetype='application/pdf')
updated = drive.files().update(
    fileId=DRIVE_FILE_ID,
    media_body=media,
    fields='id, name, webViewLink, modifiedTime'
).execute()
```

## Key Points

- **`file://` prefix** is required for Playwright to load local HTML files
- **`wait_for_load_state('networkidle')`** ensures fonts, images, and async content are fully loaded before rendering
- **`print_background=True`** is critical — without it, dark-mode backgrounds render as white
- **Drive `.update()` replaces in-place** — the old file ID and share links continue working
- Python 3.9 warnings about end-of-life are harmless and can be ignored

## Finding the Drive File ID

List files in a specific Drive folder:

```python
results = drive.files().list(
    q="'FOLDER_ID' in parents",
    fields='files(id, name, mimeType)'
).execute()
for f in results.get('files', []):
    print(f['name'], f['id'])
```
