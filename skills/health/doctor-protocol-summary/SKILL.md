---
name: doctor-protocol-summary
description: |-
  Summarise a doctor's consult notes into a practical, print-friendly supplement
  and medication regime table. Designed for the fridge: one A4 page, clear tables,
  morning/evening checklist. Includes plain-language synopsis of diagnosis.
version: 1.0.0
author: Epictetus
metadata:
  hermes:
    tags: [health, doctor, supplements, medication, protocol, fridge, print]
    related_skills: [ocr-and-documents, health-markers-report]
---

# Doctor Consult Protocol Summary

Generate a single-A4-page supplement and medication regime from a doctor's
consult notes, optimised for fridge printing.

## Trigger

Load this skill when the user asks to:
- Create a supplement/medication schedule from a doctor visit
- Make a fridge-ready protocol summary
- Summarise "what to take and when" in plain language
- Turn complex medical notes into a practical daily checklist

## Source Documents

Doctor notes are typically in the Obsidian vault under:
`Health/Health professionals/[Doctor Name]/Consult [Date]/`

Common files:
- `Patientnotes.pdf` — doctor's clinical notes (TCPDF-generated from this clinic)
- `Paul Mason Summary and Qs.md` — user's own preparatory notes/questions
- `Follow up script before next meeting.pdf` — pathology forms
- Handouts (probiotic guides, etc.)

## Extraction (PDFs)

For TCPDF-generated PDFs from specialist clinics:

```bash
pip3 install pymupdf   # already installed on this system
python3 -c "
import pymupdf
doc = pymupdf.open('Patientnotes.pdf')
for page in doc:
    print(page.get_text())
"
```

Note: TCPDF headers (clinic address, patient info) repeat on every page
— ignore duplicate headers mentally. The notes body is what matters.

## Output Structure

Save to the same consult folder. Markdown file, one-section-per-category.

### Title

`[Patient]'s Daily Protocol — Dr [Name] ([Date])`

### Sections (in order)

Write exactly what the user asked for — no more. If they ask for supplements and medicines in a table, deliver ONLY that table. Add other sections (cautions, blood tests, checklist, etc.) only when specifically requested.

Default table columns: `# | Supplement | Dose | When`
- No Notes column unless explicitly requested
- Include brand recommendations inline where given

1. **Supplements — Daily**

2. **Medicines — Weekly / As Directed** — same columns
3. **Additional sections** — only if asked (sinus rinse, body wash, eye care, cautions, blood tests, checklist)

### Style Rules

- Plain language throughout
- **Bold** for critical warnings or key info
- Tables use standard `| pipe | syntax` with `---` header separator
- Quantities explicit, not relative

## Plain-Language Synopsis

When the user also asks for a simple explanation of the doctor's diagnosis:

1. Start with **the big picture** — one paragraph explaining what the doctor
   thinks the root cause is (e.g. "Dr Mason thinks it's fungal overgrowth,
   not MCAS")
2. **Key findings** — bullet list of the main lab results and what they mean
3. **The treatment plan** — summary table showing target area, treatment, what
   it does (use a markdown table)
4. **How it all connects** — the theory linking the findings together
5. **Bottom line** — one paragraph on the doctor's approach/philosophy

## File Location

Save in the same Obsidian consult folder as the source PDFs:

```
Health/Health professionals/[Doctor Name]/Consult [Date]/Supplement & Medicine Regime.md
```

## Update Pattern

"First draft, we'll tweak" means: write the complete draft, present it, wait
for feedback. Do NOT ask for approval on every subsection.

## Fridge PDF Generation

When the user asks to print the protocol for the fridge:

1. **Create an HTML version** styled for A4 print with Playwright
2. **Font sizing starts at:** Heading 18px, body 14px, table headers 12px. This fits one A4 page while remaining readable at arm's length.
3. **Start lean.** First draft is EXACTLY what was asked for — no cautions, checklist, blood tests, or summary unless explicitly requested. The user has corrected this behaviour. If they want only the supplement and medicine tables, give them only that.
4. **Iteration pattern:** The user will ask for size adjustments in visual terms. "Double the size" means ~1.8-2x the current. "Fit on one page" means reduce fonts/padding/line-height proportionally. Change ONLY the font sizes — keep all content. Keep the Playwright script handy — changes take 10 seconds.
5. **Script location:** Use `/tmp/print_protocol.py` as a temporary working script.
6. **If the PDF already exists and the user says they deleted it, just regenerate — don't ask which version.**
7. **When the user says "do it again as it's small" — they deleted the too-small one. Don't ask which file, don't ask what went wrong. Just bump up the font sizes and regenerate. The feedback is "too small" — respond by increasing base font size by 40-60% and regenerating to the same path.**

## Pillars (Non-Negotiable)

1. **Start minimal.** The first draft is EXACTLY what the user asked for. No extra sections (cautions, blood tests, checklists, synopses) unless specifically requested. Adding "helpful extras" means the user has to delete things they didn't ask for — this was a specific correction.
2. **The user knows what they need on their fridge.** If they want cautions, they'll ask. If they want a morning checklist, they'll ask. Don't anticipate.
3. **When the user says "make it fit one page", keep ALL content but reduce font/padding.** Don't remove content to save space unless told to.
4. **When iterating PDF formatting, the user's feedback is in visual terms — respond with HTML+font-size adjustments, not structural changes.** "Double the size" means increase base font by ~1.8-2x. "Fit one page" means reduce font size, padding, and line-height proportionally.
5. **The tables ARE the content.** Don't summarise table data in prose above or below the table. If the data is in the table, it lives in the table.

## Pitfalls

- TCPDF PDFs repeat header on every page — dedupe mentally when reading
- The user needs to PRINT this — format for A4 paper, not screen-first
- Saturday/Sunday are the reference — not just weekdays
- Some items are "alternate with" others — show both options clearly
- Probiotic sinus rinse can cause intense die-off — start with ¼ capsule
