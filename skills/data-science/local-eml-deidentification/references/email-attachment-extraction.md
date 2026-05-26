# Email Attachment Extraction

When analysing de-identified .eml files, emails often carry attached documents
(agreements, invoices, quarterly reports, schedules) as MIME attachments.
Before drawing conclusions from an email that references a document, extract
and read the actual attachment.

## How to Extract

```python
from pathlib import Path
import email
from email import policy

for eml_file in folder.glob('*.eml'):
    with open(eml_file, 'rb') as fh:
        msg = email.message_from_binary_file(fh, policy=policy.default)

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                payload = part.get_payload(decode=True)
                if payload:
                    out_path = output_dir / filename
                    with open(out_path, 'wb') as f:
                        f.write(payload)
```

## What to Expect

| Type | Count (sample session) | Contains |
|------|------------------------|----------|
| PDF | ~200 | Signed agreements, reports, invoices |
| Excel | ~80 | Management accounts, fee schedules, cash flows |
| Word | ~40 | Quarterly narrative reports |
| Images | ~50 | Property photos, signed document scans |
| Calendar | ~15 | Meeting invites |

## Survival Through De-identification

The de-identification script does `str.replace()` on the raw .eml text.
If the replacement strings don't appear in the base64-encoded attachment
payload, the attachment survives intact. In practice, PDF, Excel, and
Word attachments all passed header validation in a real 662-file batch.

## Common Attachment Finds

- **Management accounts** (Excel) — quarterly P&L, balance sheet, cash flow.
  Fee lines may show €0 for management fees (if BMM billed outside Diluca).
- **Quarterly narrative reports** (Word) — BMM's update on properties, tenants,
  compliance status. Rarely itemise fees.
- **Signed agreements** (PDF) — loan agreements, PMA, amendments.
- **Invoices** (PDF) — attorney fees, commission invoices, annual invoices.
  These are the most likely place to find evidence of ad-hoc/hourly billing.
- **Digital asset management agreements** (PDF) — separate from the PMA,
  may have their own fee structure.
