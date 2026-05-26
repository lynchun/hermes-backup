---
name: local-eml-deidentification
description: "De-identify .eml files - two approaches: (A) deterministic find-and-replace with pseudonyms for known individuals, or (B) local Ollama blanket redaction for novel PII. All data stays on the machine."
---

# Local EML De-Identification

Two approaches for de-identifying `.eml` files, depending on whether you know the PII in advance.

## Evidence-Based Analysis Methodology

When Lyndon gives you a brief or asks you to analyse a situation, **do not simply repeat back what they told you.** Three layers of work required:

1. **Understand the claims** — Read what Lyndon says happened.
2. **Go to the primary sources** — Pull dates, emails, documents, and transactions directly. Verify each claim against the original evidence.
3. **Flag gaps** — If the evidence doesn't support a claim, say so. If the evidence is silent on a point, call that out explicitly.

Lyndon wants you independently satisfied of the facts. A section titled "What the Evidence Does NOT Establish" is a strength.

### Practical Steps for Any Analysis

1. Start with the brief / verbal instructions.
2. **Read the source emails** — not summaries. Pull key threads by subject keyword, read the full chains, note who said what and when.
3. **Extract attachments** — emails often reference attached documents (agreements, invoices, accounts). Extract them as standalone files before drawing conclusions. Some attachments (management accounts, signed agreements, fee schedules) contain evidence not found in email body text.
4. **Build a timeline from email Date: headers** — parse programmatically, don't guess.
5. **Map evidence to obligations** — only after steps 1-4.
6. **Flag uncertainty** — what the evidence shows, what it doesn't, where you inferred.

### Analysis Document Structure

```
# Title

**Basis:** Direct review of [N] emails spanning [dates],
           [N] attached documents, [N] contracts.

--- content ---

## What the Evidence Does NOT Establish
- Bullet list of gaps (mandatory section)
```

## Which Approach to Use

| Scenario | Approach | Method |
|----------|----------|--------|
| You know exactly who appears in the emails (clients, family) and want consistent pseudonyms | **A - Targeted Replacement** | Deterministic find-and-replace |
| Emails from unknown/unexpected contacts, or you want blanket PII removal | **B - Ollama Redaction** | Local LLM via Ollama |

**Lyndon prefers Approach A for known individuals** - deterministic, predictable, no LLM drift. Only fall back to Approach B for truly novel PII.

## Common Prerequisites

- Python 3 (stdlib `email` module always available)
- `curl` available (for Ollama API calls in Approach B)

---

## Approach A: Targeted Pseudonym Replacement

Use when you have specific PII patterns to replace with consistent pseudonyms. No LLM needed - pure string replacement on the raw .eml file text.

### Workflow

1. **Identify the replacement rules.** For each client/family, define:
   - Email address mappings (old to new)
   - Name mappings (old to new)
   - Any other recurring strings

2. **Build an ordered replacement dictionary.** Apply replacements in a specific order to avoid interference. General rule: replace longer strings first, shorter strings last.

3. **Read the raw .eml file as text.** Apply simple `str.replace()` across the entire file content - this catches PII in headers, body, HTML attributes, and quoted-printable encoded text all at once.

4. **Save with `[DE-IDENTIFIED]` suffix** in the designated output folder. Preserve original subject line + date in headers.

### Key Design Decisions

- **Replace on raw text, not parsed headers.** Email addresses appear in multiple places (From, To, CC, DKIM signatures, message bodies, HTML `mailto:` links, X-headers). Running `str.replace()` on the whole file catches all of them cleanly. Parsing and reassembling the MIME structure risks breaking encoding or losing parts.

- **Replace longer substrings first** to prevent partial matches. Example: replace `katrinaworner@bigpond.com` before `katrina` or `worner` so the email address isnt broken mid-replacement.

- **Name replacement is case-sensitive unless mixed case is expected.** The default replacements are for how names actually appear (sentence-case, title-case in headers).

### Example Replacement Set

For the Worner/Smith family (from a real session):

| Old | New |
|-----|-----|
| `khw2095@gmail.com` | `k@gmail.com` |
| `tgrworner@gmail.com` | `t@gmail.com` |
| `katrinaworner@bigpond.com` | `k@bigpond.com` |
| `Katrina` | `Karina` |
| `Worner` | `Smith` |
| `Tim` | `Jim` |
| `Leggings` / `leggings` | `Meggings` / `meggings` |

And for regulatory numbers:

```python
ABN_RE = re.compile(r'\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b')  # ABN -> [ABN REDACTED]
ACN_RE = re.compile(r'\b\d{3}\s?\d{3}\s?\d{3}\b')           # ACN -> [ACN REDACTED]
```

Full worked example with code: `references/worner-smith-replacement-set.md`

### Pitfalls

- **Order matters.** Put email address replacements before name replacements in your script, otherwise `katrinaworner@bigpond.com` gets partially replaced first by `Worner -> Smith` and becomes `katrinasmith@bigpond.com`.
- **HTML entities.** In quoted-printable encoded HTML emails, email addresses may appear as `mailto:khw2095@gmail.com` in an `href=3D"..."` attribute. `str.replace()` catches these because `gmail.com` is decoded text. Raw `=XX` escapes wont match - apply replacements AFTER cleaning quoted-printable encoding if working on the decoded body, or apply to the ENTIRE raw file.
- **No LLM means no surprises.** What you replace is exactly what gets changed. Nothing extra is detected or missed.
- **Don't blanket-redact emails.** Lyndon's preference: only apply the specific email substitutions listed. Other email addresses (like Lyndon's `lyndon@stewardscapital.com`, third-party senders, or CC'd parties) should remain untouched unless explicitly listed in the replacement rules. Over-redaction destroys email thread context.

---

## Approach B: Ollama Redaction (Blanket)

Use for emails where you dont know all the PII in advance and want an LLM to identify and redact it. All data stays local.

### Prerequisites

- Ollama running locally with a capable model installed (8B+ recommended)
- Python 3 with `email` stdlib (always available)
- `curl` available (used to call Ollama API at localhost:11434)

### Workflow

### Step 1: Parse the .eml

Use Python's `email` module with `policy=policy.default`:

```python
import email
from email import policy

with open('file.eml', 'rb') as f:
    msg = email.message_from_binary_file(f, policy=policy.default)
```

### Step 2: Extract text body

Handle multipart messages — prefer `text/plain`, fall back to `text/html`. Strip HTML tags:

```python
import re

def extract_text_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                body = part.get_content()
                break
            elif ct == "text/html" and not body:
                body = part.get_content()
    else:
        body = msg.get_content()
    
    # Clean quoted-printable encoding artefacts
    body = re.sub(r'=3D', '=', body)
    body = re.sub(r'=E2=80=AF', ' ', body)
    body = re.sub(r'=E2=80=99', "'", body)
    body = re.sub(r'=E2=80=A6', '...', body)
    body = re.sub(r'=\n', '', body)
    body = re.sub(r'=20', ' ', body)
    
    # Strip HTML
    body = re.sub(r'<[^>]+>', '', body)
    return body.strip()
```

### Step 3: De-identify via Ollama

Call the local Ollama API at `http://localhost:11434/api/generate`. Use `temperature: 0.0` for deterministic output.

**Prompt structure:**

```
You are a PII redaction tool. Redact all personally identifiable information from the text below.

REDACT (replace with [REDACTED]):
- Full names of people
- Email addresses
- Phone numbers
- Street addresses
- AFSL numbers / licence numbers

DO NOT redact:
- Dates
- Dollar amounts, percentages, interest rates
- Company names (generic/non-identifying ones like Deloitte, Trident Trust, National Bank of Greece)
- Country/city names
- Professional titles (Adviser, Director)
- General subject matter

Keep the sentence structure readable. Replace only the identifying details.

TEXT:
{email_body}

Return only the de-identified text, nothing else.
```

### Step 4: Save output

Create `[DE-IDENTIFIED].eml` copy with:
- Headers: From/To/CC -> [REDACTED]
- Subject: original + `[DE-IDENTIFIED]` suffix
- Date: preserved
- Body: the de-identified text

## PDF De-identification

For PDF de-identification, see the dedicated **`bmm-pdf-deidentify`** skill. The canonical script and full documentation live there.

**Quick summary:** The only reliable approach for PDFs with CID fonts (complex internal character maps) is to render each page as a high-resolution image and recombine. Text replacement at the content-stream level fails because CID CMaps are often mismapped or incomplete.

```bash
# Point user to the dedicated skill for full instructions
# Script: ~/Desktop/bmm_deidentify_pdf.py
python3 ~/Desktop/bmm_deidentify_pdf.py document.pdf
python3 ~/Desktop/bmm_deidentify_pdf.py /path/to/folder/
```

**Pitfalls (PDF):**
- **CID fonts defeat content-stream text replacement.** If `pdftotext` extracts garbage, the PDF uses CID fonts. Image flatten is the only reliable fix.
- **Cairo (poppler) renders better than sips.** `sips` produces dark backgrounds and inconsistent quality. `pdftocairo -png -r 200` from poppler is the recommended renderer — gives clean white backgrounds and sharp text natively.
- **Don't use PIL's PDF save.** It uses JPEG compression internally which degrades text. Use `img2pdf` instead (lossless DEFLATE).
- **200 DPI is the sweet spot.** Screen-sharp (~1 MB per 5 pages). Lower than that and text gets fuzzy; higher than that and file sizes balloon with no visible improvement on screens.
- **Verify output.** Always run `pdftotext output.pdf - | wc -c`. If it returns >50 chars, hidden text remains. The script has built-in verification.
- **Visual redaction boxes don't strip text.** Preview's markup tools only add a visual layer. The underlying text remains extractable via `pdftotext`. For the correct method, see the `bmm-pdf-deidentify` skill.

## Address Redaction (Both Approaches)

**Lyndon's preference: only redact addresses that mention specific locations.** Do NOT blanket-redact all street addresses. Instead, define a narrow set of suburb/area names to trigger redaction on:

```python
# Example: only redact lines mentioning Manly or Umina
import re
ADDRESS_REDACT_PATTERN = re.compile(r'\b(?:Manly|Umina)\b', re.IGNORECASE)
```

This prevents over-redaction of non-identifying content like building names, PO boxes, or generic street references that don't expose client location.

### Pitfalls

- **Over-redaction frustrates the user.** Redacting every address line (street, city, postcode) destroys context needed for financial/legal emails. Redact only the suburb/area the user specifies.
- **Check the output.** After redacting, spot-check that the address mentions you intended to flag were caught, but surrounding useful content (dates, amounts, reference numbers) was preserved.
- **Narrow redaction wins.** Lyndon's preference is surgical: redact lines mentioning specific locations (e.g. Manly, Umina) rather than all address-like patterns.
- **Don't trust Date: headers blindly.** Forwarded/threaded .eml files from Outlook drag-out often contain multiple `Date:` lines scattered through the raw text — one from the Exchange delivery, others from quoted forwarded content. A naive regex or `str.replace` approach picks up ALL of them. Always parse with `email.parser` and read `msg.get('Date')` only, or if analysing raw text, use `parsedate_to_datetime()` on the first match only.
- **De-duplicate output on re-run.** If the script runs on a folder containing emails it's already processed, check whether `[stem] [DE-IDENTIFIED].eml` already exists in the output directory. If it does, skip that source file — otherwise you get `(1)`, `(2)` duplicates that clutter the output and waste disk space.
- **Keep output folder as a sibling to the source, not nested inside it.** The `Deidentified folder/` should sit alongside the source folder (same parent). Nested output dirs confuse batch processing because the script scans for `*.eml` files and may pick up its own output on re-run.

## Getting Emails Out of Outlook (macOS)

When the source emails are in **Microsoft Outlook for Mac** (not standalone .eml files):

| Attempt | Result |
|---------|--------|
| Drag all 500+ to Finder at once | Beachball/hang — Finder chokes on large batch |
| AppleScript to loop and export | Outlook's AS dictionary is slow/unreliable on large mailboxes |
| Read Outlook's SQLite DB (`Outlook.sqlite`) | Only metadata — actual content is in proprietary `HxStore.hxd` |
| Read Outlook's MIME cache (`MimeFiles/` GUID folders) | Only a handful of cached .mime files, not full inbox |

**Working approach:** Drag emails in smaller batches (20-30 at a time) from Outlook to a Finder folder. Viewer/responder emails can go in one batch, sender's replies in another. Repeat until done.

```mermaid
flowchart LR
    OL[Outlook\nBMM emails for review\n531 emails] -->|Batch drag 20-30| FD[Finder folder\n~/.eml files]
    FD -->|Point script at folder| SC[deidentify_eml.py]
    SC --> OUT[Deidentified folder/\n[DE-IDENTIFIED].eml]
```

The script accepts a folder path as argument, so you can run it once per batch as you go:

```bash
python3 deidentify_eml.py /path/to/folder/with/emails
```

Each run creates `[DE-IDENTIFIED]` copies in a sibling `Deidentified folder/` subdirectory without reprocessing already-done files.

#### Pitfall: Missing Referenced Attachments

When analyzing de-identified email chains, emails often reference attachments (agreements, invoices, schedules) that aren't embedded in the .eml text. Before drawing conclusions from an email about a document, **find and read the actual document.** See `references/email-attachment-checking-pitfall.md` for a full checklist and a real-world example where skipping the attachment led to a wrong characterization.

#### Pitfall: PDF Redaction Boxes Don't Strip Text

When preparing supporting documents (agreements, invoices, statements) for sharing alongside de-identified emails, visual redaction via Preview's markup tools does NOT remove the underlying text. The original names remain extractable via `pdftotext` or "select all → copy." For the correct method (export as images → recombine), see `references/pdf-redaction-hidden-text.md`.

## Pitfalls (Approach B only)

- **Body over ~6000 chars** may exceed the model's context window. Truncate or chunk.
- **HTML-only emails** will have garbled output from crude tag stripping. Acceptable for de-identification purposes where perfect formatting doesn't matter.
- **quoted-printable encoding** (common in Outlook/Exchange emails) needs cleaning before the LLM sees it — the `=XX` escape sequences confuse the model.
- **Inline images, attachments, digital signatures** are not preserved in the de-identified output — the focus is body text only.
- **temperature: 0.0** ensures deterministic output for the same input, but the model may still produce slightly different redaction patterns for different emails.

### Running the Script

### Deploying the Script

The canonical scripts live in the skill directory:\n```\n~/.hermes/skills/data-science/local-eml-deidentification/scripts/deidentify_eml.py\n```\n\nThe PDF script lives under the companion skill at:\n```\n~/.hermes/skills/data-science/bmm-pdf-deidentify/scripts/bmm_deidentify_pdf.py\n```\n\nCopy to Desktop for daily use:\n```bash\ncp ~/.hermes/skills/data-science/local-eml-deidentification/scripts/deidentify_eml.py ~/Desktop/\ncp ~/.hermes/skills/data-science/bmm-pdf-deidentify/scripts/bmm_deidentify_pdf.py ~/Desktop/\n```\n\nRun them:\n\n```bash\n# Emails\npython3 ~/Desktop/deidentify_eml.py /path/to/folder/           # Targeted replacement\n# PDFs\npython3 ~/Desktop/bmm_deidentify_pdf.py document.pdf            # Single file\npython3 ~/Desktop/bmm_deidentify_pdf.py /path/to/folder/        # Batch process\n```

The script:
1. Reads each `.eml` from the target folder
2. Applies replacements (Approach A) or calls Ollama (Approach B)
3. Writes `[DE-IDENTIFIED].eml` to a `Deidentified folder/` subdirectory

## Model Selection (Approach B)

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| llama3.1:8b | 4.9 GB | Good | Fast |
| qwen2.5-coder:7b | 4.7 GB | Good | Fast |
| qwen2.5-coder:32b | 19 GB | Excellent | Slow |
| gemma4:latest | 9.6 GB | Very good | Moderate |

Use the smallest model that produces correct redactions. Test on one file first.
