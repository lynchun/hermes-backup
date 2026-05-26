# Supplement Protocol Extraction & Fridge Sheet

When Lyndon asks you to extract a supplement/medicine protocol from a doctor's notes and turn it into a fridge-ready A4 printable.

## Workflow

1. **Extract** the protocol from the source (PDF, markdown, notes) using pymupdf or textutil
2. **Identify all items** — supplements (with dose, frequency, timing), medicines (dose, schedule), procedures (sinus rinse, body wash, eye care)
3. **Build tables** — one table per category. Columns: # | Supplement/Medicine | Dose | When. NO Notes columns. NO extras.
4. **Strip all bonuses** — no Quick Reference checklist, no Blood Tests follow-up list, no Cautions section, no footer flourishes, no editorialising. The user wants ONLY what they asked for.
5. **Convert to PDF** for printing: playwright HTML → PDF, A4 format, print_background=True, 10mm margins
6. **Save** to the same Obsidian folder as the source notes

## Rule: Reference Docs Are Minimal

When the user asks for a fridge summary / regime sheet / cheatsheet:
- Only include what was explicitly listed in the source.
- Tables get 4 columns max: #, Item name, Dose, When.
- No Notes column. No bonus sections. No "cautions" callout boxes added by you.
- If a caution is important, mention it verbally in your response — don't add it to the printed doc unless asked.

## Printing to PDF

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file://' + html_path)
    page.wait_for_load_state('networkidle')
    page.pdf(path=pdf_path, format='A4', print_background=True,
             margin={'top': '10mm', 'bottom': '10mm', 'left': '10mm', 'right': '10mm'})
    browser.close()
```

## Related

- `ocr-and-documents` for extracting text from PDF notes
