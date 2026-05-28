---
name: country-reference-sheets
description: "Generate multilingual country reference sheets — continent maps with labeled countries, separate definition pages. Map-based layout (no per-item images). For lists of countries organized by continent."
version: 1.0.0
author: Epictetus + Lyndon Arthurson
---

# Country Reference Sheets

Generate professional country reference guides organized by continent. Different from the item-per-image pattern (vegetables/instruments) — this uses a continent map as the visual anchor, with a numbered index of countries and separate definition pages.

## Pattern

- **Page 1:** Continent map (AI-generated, clean borders, no labels) + numbered country index (EN/中文/日本語)
- **Pages 2+:** Country definitions — one per numbered entry, all three languages

## Workflow

### Phase 1: Extract country list
The user provides a PDF or list. Parse to identify which countries belong to which continent. Start with ONE continent as a trial (Africa was the first).

### Phase 2: Generate continent map (GeoPandas + Natural Earth)
**DO NOT use AI image generation for maps.** AI cannot place numbers on correct countries or shade accurate borders. Use the GeoPandas + Natural Earth pipeline instead. Full details in the `multilingual-reference-sheets` skill at `references/continent-map-pipeline.md`.

Quick checklist:
- Natural Earth 110m shapefile at `ne_data/ne_110m_admin_0_countries.shp`
- Use `representative_point()` (not `centroid`) for marker placement — guaranteed inside polygon
- Use `scatter()` markers (not `Circle` patches) — stays round at any aspect ratio
- Mercator compensation: `ax.set_aspect(1/cos(mid_lat))`
- Unshaded land must be visibly distinct from page background (`#e8e0d0` vs `#fdfaf3`)
- Leader lines for tiny countries (area < 2.0 deg²): dot on country + line to external label
- Microstates (Liechtenstein, Monaco, etc.) are not in 110m shapefile — remove from list
- Greenland → Europe (politically Danish), Australia → Oceania (for context)
- Natural Earth name mapping: Dominican Republic → "Dominican Rep.", Czech Republic → "Czechia", etc.

Bounding boxes and settings per continent are in the reference file.

### Phase 3: Translate country names + definitions
Delegate to subagent:
```
delegate_task(
  goal="Translate [N] countries into Traditional Chinese (Taiwan, 繁體) and Japanese with 2-3 sentence definitions in all three languages.",
  context="Return JSON: [{\"en\":\"Kenya\",\"zh\":\"...\",\"ja\":\"...\",\"def_en\":\"...\",\"def_zh\":\"...\",\"def_ja\":\"...\"}]. Traditional Chinese only."
)
```

### Phase 4: Build Typst document
Use execute_code to generate a `.typ` file:

**Page 1 — Map layout:**
```typst
#set page(paper: "a4", fill: rgb("#fdfaf3"))
#image("continent_map.png", width: 100%, height: 80mm, fit: "contain")
#text(size: 7pt)[Country index:]
+ *Kenya* — 肯亞 — ケニア
+ *Uganda* — 烏干達 — ウガンダ
...
```

**Pages 2+ — Definitions:**
```typst
+ *Kenya* — 肯亞 — ケニア
#text(size: 8.5pt)[
  *EN:* Kenya is in East Africa...
  *中文:* 肯亞位於東非...
  *日本語:* ケニアは東アフリカに...
]
```

### Phase 5: Compile + QC
```bash
cd ~/Desktop/Country_Reference && typst compile guide.typ guide.pdf
```
Then QC page 1: convert to PNG with pdf2image, vision_analyze to verify map visible, list clean, no formatting glitches.

## Typst patterns for country sheets

### Page structure
```typst
// Page 1
#pagebreak()
// Page 2
#pagebreak()
// etc
```

### Definition formatting
Use `+ ` enum lists for definition entries — NOT `#grid()` or `#columns()`. Grid/columns have finicky comma syntax that breaks with multi-byte characters.

### Page numbers
Center-aligned, bottom of each page:
```typst
#align(center)[#text(size: 7pt, fill: rgb("#d4c9a8"))[— 1 —]]
```

## QC Checklist (mandatory, every compile)

After every `typst compile`, run QC before telling the user it's done:

1. **Verify page 1 is not blank:** `pdftocairo -png -f 1 -l 1` output must be >50KB (blank pages <10KB). Typst exits 0 even on corrupted source.
2. **Count index entries:** All N countries must be visible in the index. If entries 18-21 are missing, the font is too large — reduce and recompile.
3. **Check circle roundness:** Circles should be perfectly round, not oval. If oval, you used `Circle()` patches instead of `scatter()`.
4. **Check leader lines:** Tiny countries (Qatar, Lebanon, Jamaica, etc.) need visible leader lines. If the line isn't visible, linewidth < 1.0 — bump to 1.2.
5. **Check continent coherence:** Unshaded land must be visible against background. If the continent looks like disconnected green blobs, unshaded color is too close to BG.
6. **Check for fragmentation:** Narrow countries (Chile, Panama) should appear as continuous landmasses. If southern Chile looks like a separate island, switch to 50m shapefile data.
7. **Check Mercator squashing:** Europe/NA countries should look proportionally natural. If Italy looks fat or Scandinavia squashed, add `ax.set_aspect(1/cos(mid_lat))`.
2. Map must have NO text/labels — clean base for the numbered index.
3. Traditional Chinese (繁體/Taiwan) only.
4. Japanese with kanji + hiragana readings.
5. Page numbers in body, not @page margins.
6. No author credit.
7. QC before delivering — verify map visible, list clean, all countries present.
8. Same directory for .typ and images — Typst resolves paths relative to source.
