---
name: assessment-list-guide
description: Build multilanguage reference guides from Scientology assessment lists. Deterministic HTML→PDF pipeline with ComfyUI photorealistic illustrations. Matches vegetable_guide.html format exactly. Proven on fruit guide (58 items, 57MB PDF).
category: productivity
---

# Assessment List Guide Builder

## Determinism Assessment

**Pipeline is ~95% deterministic.** The only non-deterministic element is ComfyUI image generation timing (but outputs ARE reproducible with fixed seeds).

| Step | Method | Deterministic? | Time |
|------|--------|---------------|------|
| Extract items | Python/docx XML parsing | ✅ Fully | <1s |
| Translate | Hardcoded in Python dict | ✅ Fully | <1s |
| Generate HTML | Template clone of vegetable_guide.html | ✅ Fully | <1s |
| Generate images | ComfyUI SDXL, euler/normal, 768×768, fixed seed per item | ✅ Reproducible | ~45s each |
| Convert to PDF | Chrome headless | ✅ Fully | ~5s |
| QC | Vision analysis, page-by-page | ✅ Process is deterministic | ~2min |

**Total: ~45 minutes for 58 items. Bottleneck is ComfyUI GPU time (unavoidable).**

## Format specification (must match exactly)
- A4 portrait, off-white background (#fdfaf3)
- Two-column layout: text left (60-65%), image right (35-40%)
- Header: "X GUIDE" in uppercase, light olive (#3a4f1f), 20pt, letter-spacing 4pt
- Subtitle: "English · 中文（繁體）· 日本語 — Botanical Reference"
- 5 items per page
- Each item row: dotted border-top/bottom (#d4c9a8), min-height 49mm
- Item name: EN 14pt bold (#3a4f1f), ZH 13pt (#4a4a2a), JA 12pt (#6b6b4a)
- Definitions: 8pt (#5c5c3a) with language labels (6.5pt #b8a878)
- Image: 50×43mm, object-fit cover, 1px solid border (#d4c9a8), in 56mm-wide column
- Page numbers: centered, 6.5pt (#d4c9a8), format "- N -"
- Font: Helvetica Neue, Hiragino Sans, Noto Sans JP

## Pipeline

### 1. Extract items from docx
```bash
python3 -c "
import zipfile, xml.etree.ElementTree as ET
path = 'path/to/list.docx'
z = zipfile.ZipFile(path)
xml = z.read('word/document.xml')
root = ET.fromstring(xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    line = ''.join(t.text or '' for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    if line.strip(): print(line.strip())
"
```

### 2. Translate items
Hardcode all translations in a Python list of tuples:
```python
(name_en, name_zh, name_ja, image_filename, def_en, def_zh, def_ja)
```
Use Traditional Chinese (Taiwan standard) and Japanese with furigana. No API calls — fully deterministic.

### 3. Generate images via ComfyUI
**Proven working template** (euler/normal, 768×768):
```python
wf = {
    "3": {"class_type": "KSampler", "inputs": {"seed": FIXED, "steps": 20, "cfg": 7,
        "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
        "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 768, "height": 768, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["4", 1]}},
    "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "ugly, blurry, low quality, deformed, watermark, text, label, multiple objects", "clip": ["4", 1]}},
    "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
    "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "fruit", "images": ["8", 0]}},
}
```
**Prompt:** `"studio product photo of a single fresh {item}, isolated on pure white seamless background, no surface visible, no plate, no table, no fabric, no props, floating, high key lighting, no shadows on background"`

**Seed:** `abs(hash(item_name)) % 2147483647` — deterministic per item.

### 4. Build HTML
Clone vegetable_guide.html CSS exactly. Script pattern at `build_fruit_guide.py`.
Image paths: `file://{IMG_DIR}/{filename}.png`
5 items per page.

### 5. Convert to PDF
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --print-to-pdf={output}.pdf \
  --no-margins --allow-file-access-from-files {input}.html
```

### 6. QC (MANDATORY — FULL, NOT SPOT-CHECK)
1. **PRE-FLIGHT:** After images generated, verify ALL expected filenames exist and >10KB. Cross-reference build script breed names with gen script breed names — they must match exactly. Mismatch = missing images = placeholder boxes.
2. Convert ALL pages to PNG: `pdftocairo -png -f 1 -l N -scale-to 1200 guide.pdf qc_`
3. Review EVERY page, EVERY item — photo accurate? All 3 language definitions present, complete, and correct? Any filename mismatches where image shows placeholder text?
4. **Do not trust vision model descriptions alone** — vision can hallucinate seeing photos where there are placeholders. For images, also verify file existence and size >10KB.
5. Flag ALL findings in a written report
6. Fix every finding
7. Re-QC until zero findings — ONLY then is it done

**This is a professional standard with zero tolerance for missed items. The user explicitly corrected spot-checking twice. Do not deliver without completing this loop.**

## Pitfalls

### ComfyUI
- **NEVER use skill's built-in SDXL workflow** — dpmpp_2m/karras at 1024×1024 causes 500 errors on MPS
- Use euler/normal at 768×768 instead — confirmed working on macOS MPS
- First prompt attempt ("on pure white background") was too weak — SDXL added plates/fabrics
- Fixed prompt: "isolated on pure white seamless background, no surface, floating, high key"
- Fixed seeds = reproducible images
- Python 3.14 asyncio bug — launch ComfyUI directly: `cd ~/Documents/comfy/ComfyUI && .venv/bin/python main.py --listen 127.0.0.1 --port 8188`
- **CRITICAL — Python 3.14 + MPS BrokenPipeError (May 2026):** The KSampler may fail with `[Errno 32] Broken pipe` on Python 3.14.2 + MPS backend, even with euler/normal at 768x768. TQDM_DISABLE=1 and stderr redirect do NOT fix this. If every generation returns `status: error` with BrokenPipeError, abandon ComfyUI and use OpenRouter image generation instead (see `references/openrouter-image-gen.md`). Cost: ~$0.03/image.

### Filename consistency
- Breed/item names MUST match EXACTLY between build script (DOGS list) and image gen script (breed list)
- Example bug: build used "Airedale" → `airedale.png`, gen used "Airedale Terrier" → `airedale_terrier.png`. HTML showed placeholder.
- **After image generation, verify**: `python3 -c "check all build names map 1:1 to gen names"`
- Or: use the SAME source-of-truth list for both scripts (single JSON file)

### Prompt adaptation
- Food items: `"studio product photo of a single fresh {item}, isolated on pure white seamless background, no surface, no plate, no fabric, no props, floating, high key lighting"`
- Animals: `"studio photograph of a purebred {breed} dog, full body, standing on pure white seamless background, professional pet photography, isolated, no collar, no props"`
- Pattern: `"studio [photo/photograph] of [a single/purebred] {item}, [on/isolated on] pure white seamless background, no [surface/props/collar], professional [food/pet] photography"`
- `write_file` in `execute_code` prepends line numbers when content comes from `read_file`. Use `patch` tool or `write_file` with freshly-generated content
- Chrome needs `--allow-file-access-from-files` for `file://` image paths

### QC process
- NEVER skip QC — user explicitly corrected this
- Switch to reviewer hat: look for every reason it ISN'T good enough
- Compare against vegetable_guide.html gold standard side-by-side
- Document findings, fix, re-QC until clean

### Subagent delegation
- **DO NOT use `delegate_task` for translation dictionary work.** During a 5-list, ~295-item bulk build, subagents tasked with building Python translation tuples all claimed completion ("file written", "55 tuples created") but wrote EMPTY FILES. Subagent summaries frequently hallucinate file creation.
- Translation data MUST be written directly by the parent agent via `write_file`. This is deterministic and immediately verifiable.
- For speed on multi-list builds: use `write_file` sequentially (fast, ~1s per file) rather than parallel subagents.

## Reference files
- Vegetable guide (gold standard): `~/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship/vegetable_guide.html`
- Fruit guide (proven build): `~/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship/build_fruit_guide.py`
- Fruit image generator: `~/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship/gen_fruit_comfyui.py`
- ComfyUI debugging log: `references/comfyui-debugging.md` — all errors encountered and how they were resolved
