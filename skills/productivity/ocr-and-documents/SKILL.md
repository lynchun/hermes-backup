---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)."
version: 2.4.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## RTF Extraction (macOS)

macOS ships `textutil` which converts RTF/RTFD to plain text, HTML, or other formats natively — no install needed.

```bash
# RTF → plain text
textutil -stdout -cat txt document.rtf

# RTF → HTML
textutil -stdout -cat html document.rtf

# Batch convert all RTFs in a folder
textutil -convert txt *.rtf
```

This is the preferred method for RTF extraction on macOS — it preserves table structure better than raw cat.

## DOCX Extraction

Use `python-docx` as noted above. But alternatively on macOS:

```bash
# DOCX → text (macOS native, no pip needed)
textutil -stdout -cat txt document.docx
```

---

## Cross-Referencing & Data Validation

After extracting data from source documents, you may need to validate compiled records (CSVs, Obsidian notes, databases) against the source. Common workflow:

1. Extract source data using pdftotext/textutil/pymupdf
2. Read compiled records (CSVs, markdown notes)
3. Compare specific data points — date+value pairs
4. Flag discrepancies

### Common OCR/Transcription Errors in Medical Data

| Pattern | Example | Fix |
|---------|---------|-----|
| Wrong unit | Testosterone 15.4 **mmol/L** → **nmol/L** | Check source doc unit column |
| Mixed tests under one name | **Iron** marker includes TIBC (53 umol/L, ref 45-80) | Split into separate markers |
| Multiple values same date | eGFR 59 **and** 90 on same date | Different labs/reports — keep both with distinct source |
| Implausible outlier | Globulin 8 g/L (ref 23-39) | Likely OCR misread — verify against source |
| `g/L` vs `mg/L` swapped | CRP 0.4 **g/L** → 0.4 **mg/L** | Check source doc unit (30.4 g/L is impossible) |
| Missing values | Homocysteine has newer but not older values | Scan all date columns in source table |
| Missing marker entirely | ANA results exist in source but no Obsidian note | Create note if needed |

### Pitfalls

- **Blank pdftotext output** doesn't mean the PDF is empty — it may be a scanned/image PDF. Try `tesseract` or `marker-pdf` for OCR.
- **Compound RTFs** (multi-page lab reports) may contain test results in later pages not shown by `head`. Always check total line count.
- **Date fields** in lab tables may default to a reference date (e.g. 1973-04-12, the patient DOB) instead of the collection date. Verify against the header.
- **CSV column misalignment** from PDF table extraction can put values in wrong columns. Validate a handful of values against source before trusting bulk extraction.
- **`vision_analyze` model limitation:** some models (e.g. DeepSeek V4 Flash) do not support `image_url` content type in the messages array. If you get `'unknown variant \`image_url\`, expected \`text\`'`, the model cannot process images natively. Alternatives: convert PDF to JPEG via `sips` and try `tesseract` OCR, or use `marker-pdf` for scanned documents. Do NOT retry `vision_analyze` — it will fail the same way each time.

## tesseract OCR (lightweight, macOS)

When marker-pdf is too heavy (~5GB) or unavailable, use `tesseract` with image preprocessing. Available on this machine at `/opt/homebrew/bin/tesseract` v5.5.2.

### macOS path-parsing bug (critical)

Tesseract 5.5.2 on this macOS version **cannot read files with absolute paths** (e.g. `/tmp/file.png`). Always `cd` to the directory first:

```bash
# WRONG — fails silently
tesseract /tmp/document.png stdout

# RIGHT
cd /tmp && tesseract document.png stdout
```

### Pipeline for phone-screenshot PDFs (72 DPI source)

Medical PDFs are often phone photos/screenshots at native 72 DPI. Do NOT upscale — it just adds noise:

```bash
# Step 1: Convert PDF page to JPEG at native resolution
sips -s format jpeg --resampleWidth 2000 document.pdf --out /tmp/page1.jpg

# Step 2: Copy to working dir (path bug workaround)
cp /tmp/page1.jpg /tmp/work.jpg
cd /tmp && tesseract work.jpg stdout --psm 6 --oem 1
```

For multi-page PDFs, use `pdftoppm` to extract individual pages:

```bash
pdftoppm -png -r 72 document.pdf /tmp/pages
# Creates pages-1.png, pages-2.png, etc.
cd /tmp && for f in pages-*.png; do echo "=== $f ==="; tesseract "$f" stdout --psm 6 --oem 1; done
```

### OpenCV preprocessing (for noisy/shadows)

```python
import cv2, numpy as np

img = cv2.imread('input.jpg', cv2.IMREAD_GRAYSCALE)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
enhanced = clahe.apply(img)
denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
_, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite('preprocessed.png', thresh)
# Then: tesseract preprocessed.png stdout --psm 6 --oem 1
```

### PSM modes for medical tables

| PSM | Use Case |
|-----|----------|
| `3` | Fully automatic (default) |
| `4` | Single column of text |
| `6` | Uniform block of text (best for pathology tables) |
| `11` | Sparse text |
| `12` | Sparse text with OSD |

Always try `--psm 6 --oem 1` first. Fall back to `3` if results are poor.

### When tesseract returns 0 chars

1. Check image exists (`sips -g all`)
2. Apply CWD workaround (`cd /tmp && tesseract`)
3. Lower resolution to native (phone screenshots = 72 DPI, not 300)
4. Try OpenCV preprocessing
5. Install `pytesseract`: `pip3 install pytesseract`
6. Fall back to `marker-pdf` (~5GB)

---

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
