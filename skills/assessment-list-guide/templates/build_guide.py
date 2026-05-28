#!/usr/bin/env python3
"""Assessment List Guide Generator — deterministic pipeline.
Clone this for each new assessment list. Replace ITEMS and GUIDE_NAME.
Usage: python3 build_{list}_guide.py
Output: {list}_guide.html → {list}_guide.pdf (via Chrome)
"""
import os, subprocess

BASE = "/Users/lyndonarthurson/ORG BOARD/Div 6 (New Contacts, PR)/PUBLIC RELATIONS/Volunteer Work/Internship"
GUIDE_NAME = "X GUIDE"  # CHANGE ME: e.g. "DOG GUIDE"
IMG_DIR = f"{BASE}/X_img"  # CHANGE ME
OUT_HTML = f"{BASE}/X_guide.html"  # CHANGE ME
OUT_PDF = f"{BASE}/X_guide.pdf"  # CHANGE ME

# ─── ITEMS ────────────────────────────────────────────────────────
# Format: (en_name, zh_name, ja_name, image_filename, def_en, def_zh, def_ja)
ITEMS = [
    # CHANGE ME: add all items here
    # ("Apple", "蘋果", "りんご", "apple.png",
    #  "A round fruit with crisp flesh.", "蘋果是一種圓形水果。", "りんごは丸い果物です。"),
]

# ─── HTML GENERATION (DO NOT MODIFY — matches vegetable_guide.html) ─
ITEMS_PER_PAGE = 5
pages = [ITEMS[i:i+ITEMS_PER_PAGE] for i in range(0, len(ITEMS), ITEMS_PER_PAGE)]

html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>''' + GUIDE_NAME + '''</title>
<style>
  @page { size: A4; margin: 8mm 6mm 4mm 6mm; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Helvetica Neue', Arial, 'Hiragino Sans', 'Noto Sans JP', sans-serif; color: #2d2d1a; background: #fdfaf3; }
  .page { page-break-after: always; padding: 5mm 0 0 0; }
  .page:last-child { page-break-after: auto; }
  .title { text-align: center; margin-bottom: 3mm; padding-bottom: 2mm; border-bottom: 1.5px solid #c4b998; }
  .title h1 { font-size: 20pt; letter-spacing: 4pt; color: #3a4f1f; font-weight: 300; text-transform: uppercase; }
  .title p { font-size: 9pt; color: #8c8056; margin-top: 1.5mm; letter-spacing: 1pt; }
  .row { display: flex; border-bottom: 1px dotted #d4c9a8; min-height: 49mm; page-break-inside: avoid; }
  .row:first-child { border-top: 1px dotted #d4c9a8; }
  .info { flex: 1; padding: 2mm 4mm; display: flex; flex-direction: column; justify-content: center; }
  .name-en { font-size: 14pt; font-weight: 600; color: #3a4f1f; }
  .name-zh { font-size: 13pt; color: #4a4a2a; margin-top: 1mm; }
  .name-ja { font-size: 12pt; color: #6b6b4a; }
  .def { font-size: 8pt; color: #5c5c3a; margin-top: 2mm; line-height: 1.5; }
  .def-en { color: #4a4a2a; }
  .def-zh, .def-ja { margin-top: 1mm; }
  .lang-label { font-size: 6.5pt; color: #b8a878; text-transform: uppercase; letter-spacing: 0.5pt; margin-right: 2mm; font-weight: 600; }
  .image { width: 56mm; min-width: 56mm; display: flex; align-items: center; justify-content: center; background: #f8f4e8; border-left: 1px dotted #d4c9a8; padding: 2mm; }
  .image img { width: 50mm; height: 43mm; object-fit: cover; border-radius: 2px; border: 1px solid #d4c9a8; }
  .page-num { text-align: center; font-size: 6.5pt; color: #d4c9a8; letter-spacing: 2pt; padding-bottom: 1mm; }
  @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
</style>
</head>
<body>
<div class="title">
  <h1>''' + GUIDE_NAME + '''</h1>
  <p>English · 中文（繁體）· 日本語 — Botanical Reference</p>
</div>
''')

for page_idx, page_items in enumerate(pages):
    html_parts.append(f'<div class="page">')
    for en, zh, ja, img_file, def_en, def_zh, def_ja in page_items:
        img_path = f"file://{IMG_DIR}/{img_file}"
        html_parts.append(f'''  <div class="row">
    <div class="info">
      <div class="name-en">{en}</div>
      <div class="name-zh">{zh}</div>
      <div class="name-ja">{ja}</div>
      <div class="def">
        <div class="def-en"><span class="lang-label">EN</span>{def_en}</div>
        <div class="def-zh"><span class="lang-label">中文</span>{def_zh}</div>
        <div class="def-ja"><span class="lang-label">日本語</span>{def_ja}</div>
      </div>
    </div>
    <div class="image">
      <img src="{img_path}" alt="{en.lower()}">
    </div>
  </div>''')
    html_parts.append(f'  <div class="page-num">- {page_idx + 1} -</div>')
    html_parts.append('</div>')

html_parts.append('</body>\n</html>')

with open(OUT_HTML, 'w') as f:
    f.write('\n'.join(html_parts))

print(f"HTML written: {OUT_HTML}")
print(f"Total items: {len(ITEMS)}")
print(f"Pages: {len(pages)} ({ITEMS_PER_PAGE} per page)")

# PDF conversion
subprocess.run([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless', '--disable-gpu',
    f'--print-to-pdf={OUT_PDF}',
    '--no-margins',
    '--allow-file-access-from-files',
    OUT_HTML
], check=True)
print(f"PDF written: {OUT_PDF}")
