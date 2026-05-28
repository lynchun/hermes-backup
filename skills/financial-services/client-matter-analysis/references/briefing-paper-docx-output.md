# Briefing Paper .docx Output Workflow

When the deliverable is a formatted `.docx` briefing paper for client review or solicitor handoff, use this workflow. For markdown-only analysis, use the main SKILL.md workflow.

## Section Structure for Client-Facing Briefing (.docx)

1. **Part 1: What [Provider] Owed the Client — Legally and Ethically**
   - Table of key contractual obligations with plain-English meaning
   - Ethical duties beyond the written contract

2. **Part 2: What [Provider] Actually Did**
   - What they got right (fairness matters)
   - What went wrong (organised by issue, not chronologically)

3. **Part 3: Timeline**
   - Clean chronological table of key events (10-15 max)

4. **Part 4: Rights, Breaches, and Options**
   - Rights violated (bullet points)
   - Provider's legal position and likely defences
   - Client's options (from simplest/cheapest to most complex)

5. **Part 5: Legal Concepts in Simple Terms**
   - 7-8 concepts, one paragraph each, no jargon

6. **Summary of Recommendations**
   - Numbered action items the client can take

## Writing Voice for Client Briefings

Write as if a knowledgeable adviser is explaining the situation directly to the clients ("you" and "your" throughout):
- "Karina and Jim, this briefing explains what happened..."
- Use headings, subheadings, and short paragraphs
- Tables for comparative information
- Bullet points for lists of issues or rights
- **No legalese.** Every legal concept gets a plain-English explanation
- **No hedging.** State the position clearly: "BMM appears to be in breach on three fronts" not "it could be argued that..."
- End with a summary of recommended actions in numbered steps

## .docx Production with python-docx

Install: `pip3 install python-docx`

### Document Setup

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
```

### Formatting Elements

- **Title page:** Center-aligned, "CONFIDENTIAL" in red, document title, date
- **Tables:** `doc.add_table(rows=N, cols=3)` with `style = 'Light Grid Accent 1'` for obligation tables
- **Timeline tables:** `cols=2` — Date | Event
- **Headings:** Level 1 for parts, Level 2 for sections, Level 3 for subsections
- **Bullet lists:** `doc.add_paragraph(text, style='List Bullet')`
- **Numbered lists:** `doc.add_paragraph(text, style='List Number')`
- **Italics:** For disclaimers and quotes
- **Bold sparingly:** Only for emphasis on key legal terms or warnings

### Disclaimer

End every briefing paper with an italicised closing paragraph:

*"This briefing is based on the [documents reviewed]. It is intended to help you understand your situation and make informed decisions. It is not legal advice."*

### File Naming

`BMM_Briefing_Paper.docx` — client abbreviation + document type. Save alongside the project brief.

## Pitfalls Specific to .docx Output

- **Missing the attachment.** When an email references an agreement/attachment and you don't read the actual document, you'll get the legal relationship wrong. Always search for referenced documents in the user's folder tree.
- **Misidentifying lender vs borrower.** Check the parties listed at the top of the agreement.
- **Over-explaining.** The client knows their own situation. Don't restate background they already gave you — analyse it.
- **Wrong deliverable format.** The user wants a `.docx` file they can open directly, not a markdown document.
- **Including opinions as fact.** Distinguish: (a) what the agreement says, (b) what the emails show, (c) what your analysis concludes.
- **Names in de-identified materials may be inconsistent.** One document may use different pseudonyms than another.
- **PDF redaction is unreliable.** Supporting PDFs may have been visually redacted but still contain hidden text. Verify with `pdftotext`.
- **Keep the document client-readable.** Avoid long paragraphs of dense text. Break content into tables, bullet points, and short sections.
- **Legal analysis is not legal advice.** Every briefing paper must include the disclaimer.
