---
name: typst-reference-sheets
description: "Generate multilingual reference sheets (vegetables, instruments, transport, etc.) using Typst for native PDF output — faster, smaller, higher quality than HTML→Chrome pipeline."
version: 1.0.0
author: Epictetus + Lyndon Arthurson
---

# Typst Reference Sheets

Generate professional multilingual reference guides with Typst — native PDF output, text-selectable, smaller files, deterministic.

## Why Typst over HTML→Chrome

| | Chrome PDF | Typst PDF |
|---|---|---|
| Speed | ~30s | <1s |
| Text selectable | No (raster) | Yes (native) |
| Size | ~95MB (48 items) | ~50MB estimated |
| Deterministic | Browser quirks | Always identical |
| Dependency | Chrome headless | `typst compile` |

## Prerequisites

```bash
brew install typst  # one-time
```

## Workflow

### Phase 1: Translations
Same as multilingual-reference-sheets skill — delegate translations to subagent, save JSON.

### Phase 2: Images
For botanical/food/item sheets: use `openai/gpt-5-image-mini` via OpenRouter. Same gen_ref_images.py script.

For country/geography sheets: skip AI images. Generate an accurate map via the GeoPandas + Natural Earth pipeline (see "Maps & Geography" section below).

### Phase 3: Build Typst document
Use execute_code to generate a `.typ` file from JSON data:
- Define a `#let veg(...)` template function (or generic `#let item(...)`)
- Loop over all items, calling the template
- Use `#set page(fill: rgb("#fdfaf3"))` for warm beige background
- Grid layout: text left (1fr), image right (42mm)
- Page numbers centered at bottom

### Phase 4: Compile
```bash
cd /tmp && typst compile document.typ output.pdf
```

## Template reference

The working Typst template is at `/tmp/test2.typ`. Key patterns:

```typst
#set page(paper: "a4", margin: (top: 12mm, bottom: 10mm, left: 12mm, right: 12mm), fill: rgb("#fdfaf3"))
#set text(font: ("Helvetica Neue", "Hiragino Sans"), size: 10pt, fallback: true)

#let veg(name_en, name_zh, name_ja, def_en, def_zh, def_ja, img_path) = {
  grid(
    columns: (1fr, 42mm), rows: (auto), gutter: 3mm,
    [
      #text(size: 13pt, weight: "semibold", fill: rgb("#3a4f1f"))[#name_en]
      #v(1mm)
      #text(size: 12pt, fill: rgb("#4a4a2a"))[#name_zh]
      ...
    ],
    image(img_path, width: 100%, height: 36mm, fit: "cover"),
  )
  v(1.5mm)
  line(length: 100%, stroke: 0.5pt + rgb("#d4c9a8"))
}
```

## Maps & Geography (country/reference guides)

**Do NOT use AI image generation for maps.** AI models (GPT-5-image-mini, Gemini, etc.) cannot do political borders, country names, or geographic positions. They shade wrong countries, drop numbers, and misplace markers.

**Always use GeoPandas + Natural Earth.** One-time setup:
```bash
pip3 install geopandas matplotlib
```

Full workflow in `references/accurate-maps.md`. Key points:
- Country names must match Natural Earth exactly (`'South Africa'` not `'Republic of South Africa'`)
- Use `world['name'].unique()` to list available names
- Centroids work correctly for island nations (Madagascar)
- DPI 200+ for clean print; `bbox_inches='tight'` to remove whitespace

**Map sizing for A4 portrait (proven values from 6-continent run):**
- Africa: 155mm height, 8×10 figsize
- Europe: 140mm height, 10×8 figsize
- Asia: 125mm height, 12×8 figsize (wide continent — less height to fit horizontally + 21 country index)
- North America: 140mm height, 10×9 figsize
- South America: 155mm height, 6×10 figsize (tall/narrow)
- Oceania: 155mm height, 6×8 figsize (single country, fill the page)
- Save with `facecolor='#fdfaf3'` to match beige page background
- Place map at top of page 1, numbered country list below
- Bounding boxes for each continent are in `references/continent-map-pipeline.md`

**Font size scaling for country index on map page (A4, 14mm left/right margins):**
The index below the map must match the `==` heading size on definition pages for visual consistency. Scale font size based on country count:
| Countries | Font size | Leading | Example |
|-----------|-----------|---------|---------|
| 1–5 | 14pt | 0.65em | South America, Oceania |
| 6–10 | 14pt | 0.65em | Africa |
| 11–15 | 12pt | 0.55em | Europe, North America |
| 16–21 | 9pt | 0.45em | Asia |
- Use individual `#text(size: Npt, weight: "bold")[N. Country — 中文 — 日本語]` per line — the `#text()` wrapper does NOT penetrate list blocks
- Tight leading via `#set par(leading: Xem)` before the index block
- Verify all entries fit on page 1 by compiling and checking — if the last entries are cut off, reduce font one more step

**Numbered circle styling (GeoPandas/matplotlib):**
- Use `mpatches.Circle((x, y), radius, facecolor='white', edgecolor='none', zorder=10)` — borderless white circles look clean and professional
- Set `edgecolor='none'` AND omit `linewidth` (or set to 0) to ensure no black edge
- Circle radius: 0.8 for large maps (Africa/Asia), 0.6 for medium (Europe), 0.4 for small (Oceania)
- Text inside: `ax.annotate(str(i), (x, y), fontsize=6.5, fontweight='bold', color='#3a4f1f', ha='center', va='center', zorder=11)`

## Rules
1. Copy images to same directory as .typ file (Typst resolves relative paths)
2. One template function per item type — reusable
3. Use `fallback: true` on fonts for CJK support
4. **QC the PDF before delivering.** Convert page 1 to PNG with `pdf2image` and use `vision_analyze` to verify: (a) all items fit without cutoff, (b) page numbers visible, (c) no text overflow, (d) margins balanced. Do NOT tell the user it's done until QC passes.
5. Typst compiles in <1s — iterate fast
6. **Beige background:** Use `#set page(fill: rgb("#fdfaf3"))` for warm paper aesthetic — Lyndon prefers this over plain white.
7. **No author credit.** Lyndon asked to remove "Created by Lyndon Arthurson" — just page numbers, no name.
8. **Traditional Chinese (繁體) only** — Taiwan standard, not Simplified (简体).

## Country Guide Page Structure

For continent-based country reference guides, use this proven 3-section page structure:

**Page 1 — Map + Index:**
```typst
#set page(paper: "a4", margin: (top: 10mm, bottom: 8mm, left: 14mm, right: 14mm), fill: rgb("#fdfaf3"))
#set text(font: ("Helvetica Neue", "Hiragino Sans"), size: 10pt, fallback: true)
#set heading(numbering: none)

// Title block
#align(center)[
  #text(size: 20pt, weight: "light", tracking: 3pt, fill: rgb("#3a4f1f"))[CONTINENT · 中文 · 日本語]
  #v(1.5mm)
  #text(size: 9pt, fill: rgb("#8c8056"))[English · 中文（繁體）· 日本語 — Countries of Continent]
]
#v(2mm)
#text(size: 7.5pt, fill: rgb("#666"))[Shaded countries are marked with numbered circles. Match the number to the index below.]
#v(1.5mm)

// Map — height varies by continent (see sizing table above)
#image("continent_map.png", width: 100%, height: Nmm, fit: "contain")
#v(1mm)

// Country index — font size scales with count (see table above)
#text(size: 7pt, fill: rgb("#888"))[Country index:]
#v(1mm)
#set par(leading: Xem)
#text(size: Npt, weight: "bold", fill: rgb("#3a4f1f"))[1. Country — 中文 — 日本語]
#text(size: Npt, weight: "bold", fill: rgb("#3a4f1f"))[2. Country — 中文 — 日本語]
...
#align(center)[#text(size: 7pt, fill: rgb("#d4c9a8"), tracking: 2pt)[— 1 —]]
```

**Pages 2+ — Definitions (5 countries per page):**
```typst
#pagebreak()
#align(center)[
  #text(size: 18pt, weight: "light", tracking: 3pt, fill: rgb("#3a4f1f"))[CONTINENT — COUNTRY REFERENCE]
  #v(1mm)
  #text(size: 9pt, fill: rgb("#8c8056"))[Definitions · English · 中文（繁體）· 日本語]
]
#v(3mm)
#line(length: 100%, stroke: 1pt + rgb("#c4b998"))
#v(1mm)
#text(size: 7.5pt, fill: rgb("#888"))[Countries N–M of Total]
#v(3mm)

== N. Country — 中文 — 日本語
#v(1mm)
#text(size: 8.5pt)[
  *EN:* Definition in English.
  *中文:* Traditional Chinese definition.
  *日本語:* Japanese definition with furigana readings.
]
#v(3mm)
// ... repeat for remaining countries on this page ...
#align(center)[#text(size: 7pt, fill: rgb("#d4c9a8"), tracking: 2pt)[— P —]]
```

**Key rules:**
- `==` headings produce ~14pt bold (1.2em × 10pt body) — match this on page 1 index
- Split into pages of 5 countries each after page 1
- Page numbers in body (`— N —`), not `@page` margins
- Empty line between index entries `#v(3mm)` on definition pages
- No "Created by" footer — user explicitly requested removal

- **Do NOT rely on vision_analyze for font size verification.** The vision model consistently fails to distinguish between font sizes (e.g., 10pt vs 14pt bold) and may report bold text as "regular weight" or claim formatting didn't apply when it did. If the Typst code says `#text(size: 14pt, weight: "bold")`, the PDF WILL render at 14pt bold — trust the code. Let the user verify on their actual screen; do not iterate based on vision model font size feedback.
- **CRITICAL: Never use execute_code write_file on Typst source files.** The `write_file` function inside execute_code writes `read_file` output verbatim including line number prefixes (`     1|content`). This silently corrupts `.typ` files — every line gets a doubled line-number prefix. Typst compiles with exit code 0 but produces blank/missing pages. To edit Typst files, use the standalone `write_file` or `patch` tools only — never through execute_code.
- **Verify page 1 has content after every compilation.** After compiling a Typst document, check page 1 is not blank: `pdftocairo -png -f 1 -l 1` and verify file size >50KB (blank pages are <10KB). Typst exits 0 even when the source is corrupted — the corruption manifests as silently blank output. Catch this before showing the user.

**Use `pdftocairo` for PDF page extraction (QC snapshots).** `sips` cannot select specific pages from a PDF. `pdftocairo` (from poppler, installed via `brew install poppler`) works correctly:
```bash
pdftocairo -png -f 2 -l 2 -singlefile -scale-to 1200 input.pdf output_page2
```
This produces `output_page2.png` for page 2 at high resolution. Use this for vision_analyze QC checks of specific pages.

## Pitfalls
- **Natural Earth 110m resolution excludes microstates.** Liechtenstein, Monaco, Andorra, San Marino, Malta, and Vatican City are NOT in the 110m dataset (cutoff is ~2,500 km²). If the user's country list includes microstates, either: (a) switch to the 50m or 10m resolution shapefile (larger download), or (b) remove the microstate from the list and note it. Luxembourg (2,586 km²) IS in 110m — the cutoff is between ~160 km² and ~2,500 km². Check with: `world[world['NAME'].str.contains('Liechtenstein', case=False)]` — if empty, it's excluded.
- **Vision model is unreliable for font size verification.** Do not iterate on font sizing based on vision_analyze feedback — the model cannot distinguish 10pt from 14pt, nor bold from regular weight. Trust the Typst code. Let the user verify visually.
- **Typst resolves image paths relative to the .typ file location.** Copy all images to the same directory as the .typ file and use bare filenames. Absolute paths like `/Users/...` get prepended with the .typ file's directory path and break.
- **Font fallback:** `#set text(font: ("Helvetica Neue", "Hiragino Sans"), fallback: true)` — the `fallback: true` flag is critical for CJK character rendering. Without it, Chinese/Japanese characters may render as tofu (□).
- **Do NOT use `#grid()` or `#columns()` with CJK text.** The comma syntax is extremely finicky and breaks unpredictably with multi-byte characters. Use flat `+ enum` lists or simple paragraph text instead. Grid/columns are only safe with pure ASCII numeric data.
- **Typst `#text()` function cannot be called inside markup cell content** — `#grid(... [*1*] #text(...))` is invalid. Functions can only appear in code mode, not inside `[…]` content blocks.
- **`#text()` wrapper does NOT penetrate list blocks.** Wrapping a list in `#text(size: 14pt, weight: "bold")[- item1 ...]` silently ignores the formatting — list items render at default body size. Use individual `#text()` calls per line instead: `#text(size: 14pt, weight: "bold")[1. Item]` on each line. The wrapper only works for inline/paragraph content, not block-level list structures.
- **Map page index must match definition page heading size for visual consistency.** Typst `==` level-2 headings render at 1.2em (14pt when body is 10pt). Use this same explicit size on the map page country index so the two pages feel like one document. 14pt bold with tight leading (~0.65em) fits 10 countries below the map on A4.
- **Map-based layouts (countries):** Place the map image at the top of the page (~140mm height, dominant visual), then a numbered list below. Use `enum` lists (`+ item`) for the index. This avoids the visual-clutter problem of trying to fit small country outline images next to definitions.
- **Chrome headless `@page` margin boxes don't work in Typst either** — put page numbers in the body content, not CSS `@page` directives.
- **AI image generation cannot do accurate geography.** See "Maps & Geography" section above for the GeoPandas + Natural Earth pipeline. Never prompt an AI model for shaded countries or numbered map markers.