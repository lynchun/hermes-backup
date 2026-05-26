# PDF Redaction: The Hidden-Text Problem

PDF "redaction" via Preview's markup tools (boxes, highlight, black rectangles) does NOT actually remove the underlying text. The original text remains in the file and is extractable via `pdftotext`, PDF readers with text selection, or any PDF parser. The boxes are visual-only annotations.

## The Problem

When you:
1. Open a PDF with sensitive names
2. Draw black rectangles over the names
3. Save the file

The names are still there. `pdftotext`, Spotlight, and "select all → copy" can all retrieve them. The PDF has two layers: a visual layer (the boxes) and a text layer (the original words). The boxes only affect the visual layer.

## What Doesn't Work

| Method | Result |
|--------|--------|
| Preview → markup black box → Save | Text still underneath — FAIL |
| Print → PDF → Save as PDF | Text layer preserved — FAIL |
| PDF Expert redaction (annotation) | Same problem — FAIL |

## What Works

### Method 1: Export as Images (guaranteed)

1. Open PDF in **Preview**
2. **File → Export...** → Format: **PNG** → Save
3. Repeat for each page
4. Open all PNGs in Preview
5. Select all → **File → Print**
6. In the print dialog, click **PDF dropdown → Save as PDF**

This produces a flat-image PDF. Every page is a photograph of what was visible. No hidden text survives because there is no text layer.

### Method 2: macOS Automator (batch)

Can use the "Convert Images" workflow if you have multiple PDFs.

## Verification

After redaction, verify no hidden text remains:

```bash
pdftotext /path/to/redacted.pdf /tmp/check.txt
grep -i "original-name" /tmp/check.txt
```

If any original names appear, the text layer is still intact.

## Best Practice

For any PDF that contained sensitive data:

1. **First pass:** Apply visual redaction (boxes, black rectangles) to what the human should see
2. **Second pass:** Export all pages as images → recombine into PDF
3. **Third pass:** Verify with `pdftotext` that no hidden text remains

Never distribute a PDF that has only been visually redacted.
