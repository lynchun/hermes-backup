---
name: multilingual-reference-sheets
description: "Generate multilingual reference sheets (vegetables, fruits, instruments, transport, countries, etc.) — English/Chinese/Japanese with AI-generated botanical-style images, print-optimized HTML, 5 items per page."
version: 1.0.0
author: Epictetus + Lyndon Arthurson
---

# Multilingual Reference Sheets

**NOTE: For item-based reference sheets (fruits, vegetables, dogs, instruments, transport), prefer the `assessment-list-guide` skill.** It has the proven deterministic ComfyUI→HTML→Chrome pipeline with exact vegetable_guide.html format matching. This skill is retained for country/geography sheets and as a general reference.

Generate professional multilingual reference guides — English, Traditional Chinese (繁體), Japanese — with AI-generated images or maps. 5+ items per A4 page, print-optimized.

**Prefer Typst pipeline.** The HTML→Chrome approach still works but Typst (`typst-reference-sheets` skill) produces native PDFs that are smaller, text-selectable, and compile in <1s. Use Typst for all new projects. The HTML pipeline is FALLBACK ONLY.

**For country/geography reference sheets:** See `typst-reference-sheets` skill "Maps & Geography" section for the full GeoPandas + Natural Earth pipeline. Six continents fully proven. The `references/continent-map-pipeline.md` file in THIS skill has all bounding boxes, Natural Earth name mappings, Mercator compensation math, font sizing tables, and pitfalls. Always load it before starting a country reference project.

**Always QC before delivering.** Use direct `vision_analyze` on pdftocairo-converted pages (not subagent — delegate_task crashes). QC every page, not just page 1. The `qc-review` skill has the checklist template and fallback patterns.

## Workflow

### Phase 1: Get translations + definitions
Delegate the translation task to a subagent. **Use Traditional Chinese (繁體, Taiwan), NOT Simplified (简体, Mainland):**
```
delegate_task(
  goal="Translate [ITEMS] into Traditional Chinese (Taiwan, 繁體) and Japanese with short 1-sentence definitions in all three languages.",
  context="Return as JSON array: [{\"en\":\"...\",\"zh\":\"...\",\"ja\":\"...\",\"def_en\":\"...\",\"def_zh\":\"...\",\"def_ja\":\"...\"}]. Chinese MUST be Traditional (繁體/Taiwan), NOT Simplified (简体/Mainland). Use proper Taiwan-standard names. Japanese with kanji + hiragana readings.",
  toolsets=["web","terminal"]
)
```
Save output to `~/Desktop/[project]_data.json`.

### Phase 2: Generate images

**For botanical/food/item reference sheets:** Use `openai/gpt-5-image-mini` via OpenRouter for consistent botanical-style images:
```bash
python3 ~/.hermes/scripts/gen_ref_images.py [project]_data.json [output_dir]
```
Prompt per image: "A professional botanical illustration of fresh [item] on a pure white background. Scientific reference style, detailed, natural lighting. No text, no labels, no borders. Square format."

**For country/geography reference sheets:** Skip AI image generation entirely — use GeoPandas + Natural Earth for accurate continent maps with shaded countries and numbered circles. The full pipeline (setup, bboxes, sizing, name matching, microstate handling) is documented in the `typst-reference-sheets` skill under "Maps & Geography" and `references/continent-map-pipeline.md`. Six continents fully proven: Africa, Europe, Asia, North America, South America, Oceania.

Run in background: `terminal(background=true, notify_on_complete=true)`

### Phase 3: Build HTML
Use execute_code to read the JSON data, map images to items, and build the HTML with:
- Warm paper background (#fdfaf3)
- Two-column layout: info (left) + image (right)
- 5 rows per page, print-optimized CSS with @page A4
- Footer: "Created by Lyndon Arthurson" in small italic
- NO URLs, NO metadata, NO ugly text
- Absolute image paths (file://...) for reliability

### Phase 4: PDF generation (Typst — preferred) or Chrome headless (fallback)

**Preferred: Typst** — native PDF, text-selectable, no browser dependency.
```bash
typst compile document.typ output.pdf
```
Typst 0.14.2+ installed via `brew install typst`. Writes `.typ` source, runs compiler. Advantages over Chrome: native vector PDF (text selectable), deterministic, smaller files, proper typesetting engine.

Key Typst patterns:
- `#set page(paper: "a4", margin: (...))`
- `#set text(font: ("Helvetica Neue", "Hiragino Sans"), fallback: true)`
- `image(path, width: 100%, height: 36mm, fit: "cover")` for vegetable photos
- Put page numbers in body, not `@page` margins (same Chrome limitation)
- Copy images to same directory as `.typ` file — Typst resolves paths relative to source

**Fallback: Chrome headless** — use only if Typst is unavailable.
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="output.pdf" \
  --no-pdf-header-footer \
  "file:///path/to/file.html"
```
The `--no-pdf-header-footer` flag is critical — without it Chrome adds URL/date stamps.

### CSS pattern for footer + page numbers
**CRITICAL: Chrome headless does NOT support CSS `@page` margin boxes (`@bottom-center`, `@bottom-right`).** These only work in browser print dialogs, not headless PDF. Instead, embed footer content as HTML elements in the body — add a `.page-footer` div at the bottom of each `.page` container with the page number. Example:
```css
.page-footer { text-align: center; font-size: 6.5pt; color: #d4c9a8; letter-spacing: 2pt; padding-bottom: 1mm; }
```
```html
<div class="page-footer">— 1 —</div>
```
Do NOT put "Created by Lyndon Arthurson" — Lyndon asked to remove his name from the document footer. Page numbers only.

### Image model: openai/gpt-5-image-mini on OpenRouter
Do NOT use Google Gemini image-preview models — they encrypt image output and OpenRouter returns `content: null`.
Use `openai/gpt-5-image-mini` which returns images in `message.images[0].image_url.url` as `data:image/png;base64,...`.
The images field is separate from content — parse `msg.get('images', [])` not `msg['content']`.

## Pitfalls
- **CRITICAL: Never pass read_file output to write_file in execute_code.** `read_file` returns content WITH line-number prefixes (`"     1|content"`). `write_file` writes it verbatim, corrupting Typst source files. The file compiles with exit 0 but produces blank pages. Pattern: use the `patch` tool for all text edits — never read_file→write_file in execute_code for source files. If you must use execute_code, strip the `N|` prefix from each line before writing.
- **Country index overflow on page 1.** With many countries (16+), the bold index list below the map overflows the page — entries silently disappear off the bottom. Typst gives NO warning. Scale font size dynamically per continent:
  - ≤10 countries: 14pt bold, 0.65em leading
  - 11–15 countries: 11–12pt bold, 0.5em leading
  - 16–20 countries: 10pt bold, 0.45em leading
  - 21+ countries: 9pt bold, 0.45em leading
  Always compile and convert page 1 to PNG to verify the LAST index entry is visible. Do NOT assume — the overflow is silent. Full table in `references/continent-map-pipeline.md`.
- **OpenRouter image generation is NOT free.** The `gen_ref_images.py` script using `gpt-5-image-mini` costs ~$0.05-0.07 per image. A 48-item reference sheet = ~$3.00. For free image generation, use **ComfyUI** (local, zero cost) — see the `comfyui` skill. Run the comfyui readiness check first: `curl -s http://127.0.0.1:8188/object_info` to confirm checkpoints are installed. If ComfyUI has models, skip Phase 2's OpenRouter script entirely and generate images via ComfyUI batch workflows instead.
- **Chrome headless ignores `@page` margin boxes.** `@bottom-center`, `@bottom-right` CSS does NOT render in headless PDFs. Embed page numbers as HTML elements in the body instead.
- **Do NOT use weasyprint** — missing system libs on macOS (libgobject). Chrome headless is the reliable path.
- **Do NOT use cupsfilter** — produces broken 68-byte stubs for HTML input.
- **Do NOT use Gemini image models on OpenRouter** — output is encrypted, content returns null.
- **Absolute image paths** (`file:///Users/...`) are required in the HTML. Relative paths break in headless Chrome.
- **Verify `<img>` tags exist** before generating PDF — `grep -c '<img src=' file.html`. If count is 0, the build script failed silently. This happens when the `<!-- DYNAMIC CONTENT -->` insert marker was already consumed by a previous run.
- **Leader lines for tiny countries.** Countries with area <2.0 deg² (Qatar, Lebanon, Caribbean islands) cannot fit a numbered circle without border overlap. Use leader lines: small dot on country → visible dark line (1.2pt, not 0.6pt which is invisible at map scale) → full circle placed 4% of map width away from continent center. Check visibility: convert page 1 to PNG at 1400px and verify lines are actually visible. Thin lines disappear at map resolution.
- **Footer in HTML body, not CSS @page.** Chrome headless won't render `@bottom-center`/`@bottom-right`. Put page numbers in a `.page-footer` div inside each `.page` container.

## Template CSS (copy-paste)
The standard stylesheet is in the vegetable_guide.html reference at:
`/Users/lyndonarthurson/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship/vegetable_guide.html`

## Rules

### Language
- **Traditional Chinese (繁體) for Taiwan** — NOT Simplified Chinese (简体). Lyndon requires Taiwan-standard Traditional characters for all reference sheets.

### Delivery quality
1. **Never deliver HTML with placeholder images.** Generate all images before telling the user the document is ready.
2. **Test one image first** before batch generating. Verify it's a real botanical photo, not an SVG/emoji/blank.
3. **Verify `<img>` tags exist** in the HTML (`grep -c '<img src=' file.html`). If count is 0, the build script ran but failed silently — a common pitfall where the insert marker was already consumed by a previous run.
4. **QC the PDF.** After generation, convert page 1 to PNG via `pdf2image` and use `vision_analyze` to check: (a) all 5 items fit without being cut off, (b) page numbers visible, (c) no text overflow, (d) margins look balanced. Do this BEFORE telling the user.
5. **Use execute_code** for HTML assembly — it handles JSON + file I/O cleanly without giant terminal commands.
6. **Background image generation** via `terminal(background=true, notify_on_complete=true)` — lets user continue other work.
7. **No URLs, no dates, no metadata, no author credit** in the final output. Only: title, subtitle, content, images, page numbers. Lyndon explicitly asked to remove his name.
8. **Print-optimized CSS** — `page-break-inside: avoid` on `.row`, `@page { size: A4 }`, Chrome `--no-pdf-header-footer`. Footer/page numbers go in HTML body (`.page-footer` div), NOT in CSS `@page` margin boxes.
