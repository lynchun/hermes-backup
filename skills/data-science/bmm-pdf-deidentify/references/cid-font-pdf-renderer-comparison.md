# PDF Renderer Comparison: sips vs PIL vs pdftocairo

## The Problem

Need to flatten PDFs to image-based copies that strip ALL hidden text layers
while preserving readable quality and reasonable file size.

## Options Tested

| Renderer | Quality | Background | File Size | Verdict |
|----------|---------|------------|-----------|---------|
| `sips -jpeg` | Poor | Dark/black | Small | FAIL — dark background, JPEG artifacts degrade text |
| `sips -png` + PIL composite | Good after white fix | Transparent → composited | Medium | FAIL — PIL.save() uses JPEG internally, degrades text |
| `sips -png` + img2pdf | Good after white fix | Transparent → composited | Medium | BETTER — lossless DEFLATE, but sips render quality is inconsistent |
| `pdftocairo -png` (Cairo, 600 DPI) + img2pdf | Excellent | White (native) | Large (3x) | BEST — Cairo's sub-pixel anti-aliasing produces sharp text. File sizes large at 600 DPI. |
| `pdftocairo -png` (Cairo, 200 DPI) + img2pdf | Very good | White (native) | ~0.9 MB / 5 pages | WINNER — screen-sharp, small files, clean white background |

## Key Learnings

1. **sips renders PDFs on a transparent/dark background.** Many PDFs don't have
   an explicit white page fill. sips renders transparent pixels as black or dark
   (RGBA 0,0,0,0). White background must be composited in post-processing.

2. **PIL's `Image.save()` as PDF uses JPEG internally.** Even with `quality=95`,
   JPEG is lossy. Text with thin strokes (legal documents, spreadsheets) shows
   compression artifacts. Use `img2pdf` instead — it embeds the original PNG
   using lossless DEFLATE.

3. **Cairo (pdftocairo) renders natively on white.** No compositing needed.
   The background is clean white (R=252, G=252, B=252 in testing).

4. **200 DPI is the practical ceiling for on-screen reading.** Higher DPI
   quadruples file size with no visible improvement on Retina displays.
   The relationship is: 2x DPI → 4x pixels → ~4x file size.

5. **Always verify with pdftotext.** After flattening, run `pdftotext output.pdf - | wc -c`.
   If >50 chars remain, hidden text survived the process. Cairo at 200 DPI
   produces 0-5 chars (whitespace artifacts only).

## Instructions for Replacing sips with Cairo

```bash
# Install poppler (one time)
brew install poppler

# Render pages
pdftocairo -png -r 200 input.pdf /tmp/pages/page

# Combine into PDF
pip3 install img2pdf
python3 -c "
import img2pdf, os
pages = sorted(['/tmp/pages/' + f for f in os.listdir('/tmp/pages') if f.endswith('.png')])
with open('output.pdf', 'wb') as f:
    f.write(img2pdf.convert(pages, dpi=200))
"
```

## File Size Comparison (19-page PMA document)

| Method | Size | Quality |
|--------|------|---------|
| sips 4000px + PIL JPEG | 6.4 MB | Degraded |
| sips 4000px + white + PIL JPEG | 7.1 MB | Degraded (white bg) |
| pdftocairo 600 DPI + img2pdf | 23 MB | Perfect (overkill) |
| pdftocairo 200 DPI + img2pdf | 6.8 MB | Perfect (screen) |
