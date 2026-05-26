---
name: bmm-pdf-deidentify
description: "Flatten PDFs to clean, non-searchable copies using Cairo at 200 DPI. Removes ALL hidden text layers. Uses pdftocairo + img2pdf. Built-in verification via pdftotext."
---

# BMM PDF De-identification (Cairo Flatten)

Render PDF pages using Cairo (poppler) at 200 DPI, then recombine into a lossless PDF. Removes ALL hidden text layers, metadata, and annotations. Built-in verification step confirms no extractable text remains.

**Script:** `~/Desktop/bmm_deidentify_pdf.py`

## Pipeline

`Original PDF → pdftocairo (200 DPI) → PNGs → img2pdf (DEFLATE) → Clean PDF ✓ → pdftotext verification`

## Prerequisites

- `poppler` (`brew install poppler`) — provides `pdftocairo`
- `img2pdf` (`pip3 install img2pdf`)
- Python 3

## Usage

```bash
# Single file
python3 ~/Desktop/bmm_deidentify_pdf.py document.pdf

# Custom output path
python3 ~/Desktop/bmm_deidentify_pdf.py input.pdf output.pdf

# Batch folder
python3 ~/Desktop/bmm_deidentify_pdf.py /path/to/folder/
```

Output is named `[original] [DE-IDENTIFIED].pdf` alongside the source.

## Quality & Size

| DPI | 5 pages | 19 pages |
|-----|---------|----------|
| 200 | ~0.9 MB | ~7 MB |

200 DPI is double standard screen resolution — text is sharp and crisp. File sizes are practical for email and document management.

## Verification

The script automatically runs `pdftotext` on every output. If more than 50 characters of hidden text remain, it prints a WARNING. All tested documents achieve 0-5 chars (whitespace artifacts only).

## PRIVACY RULE — Agent Must NOT Read Client Documents

When a user asks to de-identify client documents — **do NOT read, view, analyse, or inspect the contents.** No `read_file`, `vision_analyze`, or browser tools. Run the script via `terminal()` and report the result. Client data never enters the agent's context window. The script's built-in verification confirms cleanliness.

## Background: Why Image Flattening

PDFs often use **CID fonts** with character maps (CMaps) that map character IDs to Unicode. In some PDFs, these CMaps are incorrect or incomplete — the visible glyphs don't match what the CMap says. This means:

- `pdftotext` extracts garbled text
- Content-stream text replacement (find-and-replace on raw operators) fails because the hex-encoded CIDs don't decode to the expected Unicode strings
- The only reliable approach is to render each page as a high-resolution image and recombine

See `references/cid-font-pdf-renderer-comparison.md` for the full comparison of renderers tested (sips, PIL, img2pdf, pdftocairo) and why Cairo was the winner.

## Pitfalls

- **CID fonts defeat content-stream text replacement** — the hex codes in TJ/Tj operators don't map to readable ASCII. Don't try to edit the content stream; flatten to images.
- **Visual redaction boxes don't strip text** — Preview's markup tools only add a visual layer. The underlying text remains extractable via `pdftotext`.
- **200 DPI is enough** — higher DPI (600+) produces files 3-4x larger with no visible improvement on screens. For print-quality needs, the user can adjust the script's `-r` flag manually.
- **Verify every output** — the script does this automatically. If the user reports hidden text, check with `pdftotext output.pdf - | wc -c`.
- **Output can't be searched** — since all text is rasterized, the output PDF has no selectable text. If the user needs searchable output, they'd need OCR on the result. This is a trade-off of the approach.
