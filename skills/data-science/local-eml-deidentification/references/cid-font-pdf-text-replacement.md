# CID Fonts and Why Text Replacement Fails on Some PDFs

Some PDFs use CID (Character ID) fonts with embedded font programs. In these PDFs, the visible text is NOT stored as ASCII or Unicode strings. It's stored as character IDs mapped through a font program to glyph outlines. The ToUnicode CMap that's supposed to help extractors decode the text is often incomplete, wrong, or missing entirely.

## The Problem

When you run pdfminer, pdftotext, or pikepdf on a CID-font PDF:

```python
page.extract_text()  # may return garbled text or nothing useful
```

And raw content stream manipulation:

```python
stream = page['/Contents']
data = stream.read_bytes()
# data contains hex codes like <0057><004c>...
# These do NOT map to 'Worner' via the CMap
```

The CMap says CID 0x57 -> U+0074 ('t'), but the actual glyph at that position renders as 'W'. The font creator put different glyphs at these CIDs than what the ToUnicode CMap claims.

This means:
- str.replace() on the raw content stream won't find your target text because the text is CID-encoded, not ASCII
- pypdf/pikepdf text extraction may return garbage, making regex replacement impossible
- Commercial PDF editors sometimes handle this, but open-source tools generally cannot

## The Only Reliable Fix: Image Flattening

Since the text cannot be reliably decoded or replaced at the content-stream level, the only guaranteed approach is:

1. Convert each page to a lossless image (PNG at 4000px / 300 DPI)
2. Recombine the images into a new PDF

This removes ALL text layers, metadata, and annotations. The visible glyphs are preserved as pixels.

## Detection

Check if a PDF uses CID fonts before processing:

```python
import pikepdf
with pikepdf.open('doc.pdf') as pdf:
    page = pdf.pages[0]
    fonts = page['/Resources']['/Font']
    for name, font in fonts.items():
        subtype = font.get('/Subtype', '')
        encoding = font.get('/Encoding', '')
        has_cmap = '/ToUnicode' in font
        print(f'{name}: subtype={subtype}, encoding={encoding}, has_ToUnicode={has_cmap}')
```

If subtype is /Type0 and encoding is /Identity-H, the PDF uses CID fonts. Text replacement at the stream level will be unreliable.

## What NOT to Do

- Don't try to decode CID CIDs manually -- the CMap may be incorrect or incomplete
- Don't use JPEG for the flatten -- JPEG is lossy and makes text fuzzy. PNG is lossless
- Don't use low resolution -- 2000px makes legal document text hard to read. Use 4000px minimum
- Don't assume font substitution works -- even macOS Core Text won't map CIDs correctly when the CMap lies
