---
name: ocr-image-ingest
description: "Auto-detect file paths to images/PDFs pasted into the terminal, run them through the OCR pipeline (pdftoppm + OpenCV + tesseract), and return extracted text. Handles phone screenshots, scanned pathology PDFs, and standard images."
version: 1.1.0
author: Epictetus
metadata:
  hermes:
    tags: [ocr, images, pdf, tesseract, ingestion]
---

# OCR Image/PDF Ingest Skill

When the user pastes a file path (or drags a file from Finder) ending in .png, .jpg, .jpeg, .pdf, .tiff, .bmp, or .gif, use this pipeline to extract text:

## Pipeline

```bash
# For PDFs:
pdftoppm -png -r 72 "$FILE" /tmp/ocr_page
cd /tmp && tesseract ocr_page-1.png stdout --psm 6 --oem 1 2>/dev/null

# For images (PNG/JPG):
cp "$FILE" /tmp/ocr_img.png
cd /tmp && tesseract ocr_img.png stdout --psm 6 --oem 1 2>/dev/null
```

## Important Notes

1. **Tesseract path bug**: Tesseract 5.5.2 on this macOS cannot read files with absolute paths (e.g. `/tmp/file.png`). Always `cd /tmp` first and reference files by basename only.

2. **PDF screenshots**: Many PDFs from phones are actually JPEG images embedded at 72 DPI. Use `pdftoppm -r 72` (not 300) — upscaling doesn't add detail.

3. **For multiple-page PDFs**: Process each page separately:
   ```bash
   pdftoppm -png -r 72 "$FILE" /tmp/ocr_page
   for f in /tmp/ocr_page-*.png; do
     cd /tmp && tesseract "$(basename $f)" stdout --psm 6 --oem 1 2>/dev/null
   done
   ```

4. **sips fallback**: If pdftoppm fails or times out, use macOS `sips` to convert the PDF first:
   ```bash
   sips -s format jpeg --resampleWidth 2000 "$PDF" --out /tmp/ocr_sips.jpg
   cd /tmp && tesseract ocr_sips.jpg stdout --psm 6 --oem 1 2>/dev/null
   ```

5. **If tesseract returns nothing**: Run from the file's directory, not with absolute path. Try `cd /tmp && tesseract test.jpg stdout` not `tesseract /tmp/test.jpg stdout`.

6. **Return the extracted text to the user** so they can confirm it's correct before you act on it.

## When to use

Trigger when the user says anything like:
- "I have a picture/screenshot"
- "Here's a file" + pastes a path
- Drags a file from Finder into the terminal
- References an image/PDF they want you to read

## Batch Processing Many PDFs

When the user drops 45+ individual pathology PDFs (one per test), do NOT OCR each one individually. Instead:

1. First try `pdftotext -layout "$FILE" -` on a sample — most modern Australian lab reports are text-based, not image-based.
2. If that works on the first few, batch-extract all files.
3. Scan the output for lines that contain result units: `mmol/L`, `umol/L`, `g/L`, `U/L`, `nmol/L`, `pmol/L`, `mg/L`, `ug/g`, `IU/mL`, `mgA/L`, `kU/L`, `mIU/L`, `mL/min`, `pg`, `fL`, `%`, `x10`
4. Filter out boilerplate lines (Tests Completed, Tests Pending, NATA, Powered by TCPDF).
5. Group results by marker name and extract value + reference range.

## Boundaries

Do NOT use this for OCR-heavy tasks on known-good text PDFs (use pdftotext first — it's faster). Only fall back to OCR when pdftotext returns empty.

**Model limitation:** The current model (DeepSeek V4 Flash) does NOT support `image_url` content in the vision_analyze tool — that API call will fail with a 400 error. Do NOT use vision_analyze for image screenshots; always fall back to the terminal-based OCR pipeline instead. This is a model restriction, not a tool bug.
