---
name: video-promo-pipeline
description: |-
  Build a reusable HyperFrames-based video promo pipeline. Template-based:
  design the visual identity once, then swap assets per release to generate
  social-media-ready promos. For label-specific templates (Unchained Recordings
  design language) see the unchained-promo-templates skill instead.
version: 1.1.0
author: Epictetus
metadata:
  hermes:
    tags: [video, promotion, hyperframes, music, social-media, creative]
    related_skills: [hyperframes, hyperframes-cli, hyperframes-registry, unchained-promo-templates]
---

# Video Promo Pipeline

Build a reusable video promo template in HyperFrames. For the Unchained
Recordings specific design language (beat-synced editing, template styles,
logo treatments) use the `unchained-promo-templates` skill instead — it
contains the brand-specific production principles.

## System Requirements

```bash
node --version   # needs >= 22
ffmpeg -version  # needed for rendering
```

## Project Setup

```bash
npx hyperframes init my-label-promos
cd my-label-promos
```

This creates: `index.html`, `hyperframes.json`, `meta.json`, `package.json`,
`AGENTS.md`, `CLAUDE.md`.

## Template Architecture

Design the template to accept parameters per release:

1. **Intro** — label logo + visual (3-5s)
2. **Track card** — cover art, artist name, track name (5-8s)
3. **Outro** — release info + call to action (3-5s)

Total: ~15-20s, vertical 9:16 (1080x1920) for Instagram Reels / TikTok.

## Composition Rules (HyperFrames)

Key rules from the hyperframes skill — always follow these:

- <div id="stage" data-composition-id="..." data-start="0" data-width="1080" data-height="1920">
- Every timed element needs data-start, data-duration, data-track-index
- Visible timed elements must have class="clip"
- GSAP timelines must be paused and registered on window.__timelines
- Videos use muted with a separate <audio> element for audio
- No Date.now(), Math.random(), or network fetches — use seeded PRNG (mulberry32) if randomness is needed
- All timelines start { paused: true }
- Duration comes from data-duration, not from GSAP timeline length
- No repeat: -1 — calculate exact repeat count
- Never build timelines inside async/await/setTimeout/Promises

### Static HTML vs JS DOM Generation

HyperFrames frame capture reads window.__timelines synchronously on page load. If JS takes too long building the DOM (generating 75+ rows via JS) before registering the timeline, the capture engine starts before content exists, producing blank frames or delayed renders.

Do NOT dynamically generate composition content via JS at runtime (canvas drawing, JS-constructed DOM hierarchies, async data loading). Use static HTML with all elements present in the source file. CSS animations (@keyframes) handle motion reliably — reserve GSAP only for overlay effects like glitch flashes and crossfades.

When you must generate content dynamically (e.g. a large ASCII field), pre-render the HTML in a Python script and write a static .html file.

Frame capture timing: render log warnings like "Sub-composition timelines not registered after 45000ms" mean the DOM is too heavy or JS runs too long. Keep compositions under ~60-80 DOM elements for reliable capture.

## OpenRouter Vision API — Analysing Cover Art

When analysing cover art or video frames to extract design language (colours,
typography, mood), use the OpenRouter vision API. The key pattern is:

**Handling large base64 payloads:** The image must be base64-encoded. For
images over ~500KB, write the API body to a temporary file first to avoid
curl's argument-length limit ("Argument list too long"):

```bash
# WRONG — fails for large images
curl -d '{"messages":[{"content":[{"image_url":{"url":"data:image/jpeg;base64,'"$B64"'"}}]}]}' ...

# RIGHT — write body to file first
python3 -c "
import json
body = json.dumps({...})
with open('/tmp/api_body.json', 'w') as f: f.write(body)
"

curl -s https://openrouter.ai/api/v1/chat/completions -d @/tmp/api_body.json
```

Extract: dominant hex colours / hex palettes, font style (sans-serif blocky
all-caps, angular tech-style), layout composition, mood, any text treatment.

## Audio Energy Analysis

To find drop points and energy structure in a track for beat-synced editing:

```python
import subprocess, numpy as np

# Extract PCM audio
r = subprocess.run([
    'ffmpeg', '-y', '-i', 'track.wav',
    '-ac', '1', '-ar', '22050', '-f', 's16le', '-t', '90', '/tmp/raw.pcm'
], capture_output=True)

# Compute RMS energy per 100ms window
samples = np.fromfile('/tmp/raw.pcm', dtype=np.int16).astype(np.float32)
window = int(22050 * 0.5)  # 500ms windows
hop = int(22050 * 0.1)     # 100ms steps

for i in range(0, len(samples) - window, hop):
    chunk = samples[i:i+window]
    rms = np.sqrt(np.mean(chunk**2))
    db = 20 * np.log10(max(rms, 1))
```

The drop threshold is typically ~80dB (RMS). Below 75dB = build/ambient.
Above 80dB = sustained drop section.

## Face Extraction from Cover Art

To extract just the artist's face from album art for use in the Left/Right
split template:

1. **Analyse cover with OpenRouter vision** — ask for exact crop coordinates
   at full resolution
2. **Crop with Pillow** — PIL/Pillow crop at the AI-suggested coordinates
3. **Remove background** — sample the average colour from the 4 edges of the
   crop, then make pixels within ~40 RGB tolerance of that colour transparent
4. **Resize** — the face asset should be ~350x420px for a 1080x1920 composition

```python
from PIL import Image

img = Image.open('cover.png')
# Crop face area (coordinates from AI analysis)
face = img.crop((x, y, x+w, y+h)).convert('RGBA')
pixels = face.load()

# Make background-coloured pixels transparent
bg_samples = [pixels[0,0], pixels[w-1,0], pixels[0,h-1], pixels[w-1,h-1]]
bg_r = sum(c[0] for c in bg_samples) // 4
bg_g = sum(c[1] for c in bg_samples) // 4
bg_b = sum(c[2] for c in bg_samples) // 4

for py in range(h):
    for px in range(w):
        r, g, b, a = pixels[px, py]
        dr, dg, db = abs(r-bg_r), abs(g-bg_g), abs(b-bg_b)
        if dr < 40 and dg < 40 and db < 40:
            pixels[px, py] = (r, g, b, 0)

face = face.resize((350, 420), Image.LANCZOS)
face.save('assets/face.png')
```

## Font Sizing for Social Video

For a 1080x1920 vertical composition, text on the right panel should be:

- Artist name: 96px
- Track title: 82px
- EP label: 48px
- Label name: 40px
- OUT NOW: 64px

These are uniformly right-aligned. If the user says "100% bigger", increase
by ~1.8-2x from the current size. Font family is the label's custom font
(Unchained Font — blocky industrial sans-serif).

## Scene Transitions Rule

Every multi-scene composition MUST:
1. Use transitions between scenes (no jump cuts)
2. Use entrance animations on every scene (`gsap.from()`)
3. Never use exit animations except on the final scene
4. The last scene may fade elements out

## Workflow per Release

### Step 1: Asset Collection

User provides:
- Cover art (PNG or JPG) → copy to `assets/cover.png`
- Audio file (WAV master) → `assets/track.mp3`
- Artist name, EP/song title, catalogue number

### Step 2: Visual Analysis (via OpenRouter Vision)

Analyse cover art and reference videos using OpenRouter vision API before building the composition:

```bash
# Convert to JPEG for API
sips -s format jpeg -Z 800 "cover.png" --out /tmp/cover.jpg

# Analyse via OpenRouter
B64=$(base64 -i /tmp/cover.jpg)
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3-flash-preview",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe colours, typography, layout, mood..."},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,'"$B64"'"}}
      ]
    }],
    "max_tokens": 500
  }'
```

Key info to extract: dominant hex colours, font styles (sans-serif/blocky/angular, all-caps), layout composition, mood, any existing text/typography treatment.

### Step 3: Build Composition

1. Edit composition → update names, dates, colours, fonts in HTML
2. Validate → `npm run check`
3. Preview → `npm run dev`
4. Render → `npm run render`
