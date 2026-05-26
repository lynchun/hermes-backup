---
name: legal-analysis-briefing
description: Create structured legal analysis briefing papers from email evidence + supporting documents. Covers reading the brief, consolidating evidence, building a timeline, identifying rights/breaches/options, and producing a formatted .docx briefing paper in plain language.
---

# Legal Analysis Briefing Papers

Create structured client-facing analysis documents from email evidence and supporting materials. Output is a well-formatted .docx briefing paper suitable for client review, solicitor handoff, or evidence organisation.

## When to Use

- You have a large body of de-identified email correspondence (~1000+ emails over years)
- Supporting documents are available (agreements, invoices, financial statements)
- The client/project brief asks for: obligations owed, actions taken, timeline, rights violated, legal position, client options, and legal precedents explained in simple terms
- The output needs to be a proper document (not just chat text)

## Workflow

### Phase 1: Read the Brief

Start by reading the project brief. Understand:

- **Who** are the parties (client, counterparty, professionals involved)
- **What** is the engagement (agreement type, scope of work, fee structure)
- **What went wrong** (the specific issues raised in the brief)
- **What the client wants** (specific deliverable structure)

### Phase 2: Map the Supporting Documents

Before reading emails, inventory the supporting materials:

- Agreements (PMA, loan agreements, addendums) — read the key clauses
- Analysis documents (if any exist) — these may already have legal analysis
- Financial documents (loan schedules, invoices, bank statements)
- Any correspondence summaries or chronologies

**Key: Read attachments referenced in emails.** An email may mention an "attached agreement" — skipping it and relying on how the email characterises it can lead to wrong conclusions. Always find and read the actual document attachment.

### Phase 3: Extract the Key Email Evidence

With 1000+ emails, don't read every one. Instead:

1. **Use the email subjects to map conversations** — threads cluster around topics (Navarinou funds, Diluca accounts, loan terms, etc.)
2. **Read final/current emails in each thread first** — they often summarise the history
3. **Build the timeline as you go** — note key events with dates and sources
4. **Identify repeated patterns** — one-off issues vs systemic failures

Key facts to extract from the email record:

- Dates of significant events (sale, payment, freeze, notification)
- What BMM/contractor said they would do
- What they actually did (or failed to do)
- When the client was informed (vs when the client discovered)
- Any admissions or statements against interest

### Phase 4: Structure the Briefing Paper

Organise the output into these sections, matching the brief structure:

| Section | Content |
|---------|---------|
| **Part 1: Obligations Owed** | Contractual obligations (by clause), ethical duties. Written as: promise → what it means → why it matters in this case. Include a table. |
| **Part 2: What They Actually Did** | What went right (briefly), what went wrong (systematically). Each issue gets its own subsection. Include quotes from emails. |
| **Part 3: Timeline** | Chronological table. Date → Event pairs. 10-15 key events max. Covers the full period from engagement to present. |
| **Part 4: Rights, Breaches, Position, Options** | Rights violated (list with bullet points). BMM's legal position (exposure + likely defences + counter-arguments). Client options (4 options ordered from simplest/cheapest to most formal). Include a "what NOT to do" or "things to consider" section. |
| **Part 5: Legal Concepts in Simple Terms** | 7-8 concepts explained in plain language with real-world analogies. Each: concept name → one-paragraph explanation → why it applies here. |

### Phase 5: Write in Plain Language

The audience is the client, not a lawyer. Use plain English:

- Short sentences (under 25 words where possible)
- No Latin terms (use "set-off" not "set-off", "before" not "prior to")
- Active voice ("BMM failed to" not "it was failed to be done by BMM")
- Explain every legal concept with a real-world analogy
- Tables for lists of obligations
- Timeline table for chronology
- Headings that describe the content ("What BMM Owed You" not "Contractual Obligations")

**Voice:** The paper should read as if a knowledgeable adviser is explaining the situation directly to the clients ("you" and "your" throughout).

### Phase 6: Produce the .docx

Use `python-docx` (install with `pip3 install python-docx`). Build the document programmatically:

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
```

Use these formatting elements:

- **Title page:** Center-aligned, "CONFIDENTIAL" in red, document title, date
- **Tables:** `doc.add_table(rows=N, cols=3)` with `style = 'Light Grid Accent 1'` for obligation tables
- **Timeline tables:** `cols=2` — Date | Event
- **Headings:** Level 1 for parts, Level 2 for sections, Level 3 for subsections
- **Bullet lists:** `doc.add_paragraph(text, style='List Bullet')`
- **Numbered lists:** `doc.add_paragraph(text, style='List Number')`
- **Italics:** For disclaimers and quotes
- **Bold sparingly:** Only for emphasis on key legal terms or warnings

**File naming convention:** `BMM_Briefing_Paper.docx` — client abbreviation + document type. Save alongside the project brief.

**Disclaimer:** Include an italicised closing paragraph: *"This briefing is based on the [documents reviewed]. It is intended to help you understand your situation and make informed decisions. It is not legal advice."*

## Pitfalls

- **Don't characterise without the attachment.** An email that says "please sign the attached loan agreement amendment" could mean something very different than what you assume. Read the attachment before writing about it. For a real-world example, see `references/loan-amendment-characterisation-example.md` — a session where a 9% interest rate was initially characterised as benefiting the counterparty when it actually benefited the client as lender.Always read the referenced document.
- **Names in de-identified materials may be inconsistent.** One document may be de-identified differently from another (e.g., emails use "Smith" but the PDF still shows "Worner"). Cross-check before writing.
- **PDF redaction is unreliable.** Supporting PDFs may have been visually redacted but still contain hidden text. Verify with `pdftotext` before relying on them.
- **Legal analysis is not legal advice.** Every briefing paper must include a clear disclaimer. Analysis is for client understanding and solicitor review, not for direct action without professional legal advice.
- **Keep the document client-readable.** Avoid long paragraphs of dense text. Break content into tables, bullet points, and short sections. The client should be able to skim the headings and get the gist, then dive into sections they care about.

## Related Skills

- `local-eml-deidentification` — for de-identifying the source emails before analysis
- `plan` — for planning the work structure before diving in
