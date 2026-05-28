# ComfyUI Debugging Log — Assessment List Guides

## Error 1: 500 Internal Server Error on prompt submission

**Symptoms:** All 58 image requests returned HTTP 500. Manual test with minimal workflow (64×64, steps=1) worked.

**Root cause:** The skill's built-in SDXL workflow (`sdxl_txt2img.json`) uses `dpmpp_2m` sampler with `karras` scheduler at 1024×1024. This combination causes GPU memory issues on Apple Silicon MPS backend.

**Fix:** Use `euler` sampler with `normal` scheduler at 768×768 resolution. Same node structure, different parameters.

**Working template:**
```json
{
  "3": {"class_type": "KSampler", "inputs": {"seed": 42, "steps": 20, "cfg": 7,
    "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
    "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
  "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
  "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 768, "height": 768, "batch_size": 1}},
  "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "PROMPT", "clip": ["4", 1]}},
  "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "ugly, blurry, low quality, deformed, watermark, text, label, multiple objects", "clip": ["4", 1]}},
  "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
  "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "output", "images": ["8", 0]}}
}
```

## Error 2: Images have plates, fabrics, dark backgrounds

**Symptoms:** First batch of fruit images showed apples on plates with fabric, pears on dark gradient backgrounds. Vision model flagged "inconsistent backgrounds."

**Root cause:** Prompt was too weak: "on a pure white background" allowed SDXL to add surfaces and props.

**Fix:** Stronger prompt with negative instructions:
```
studio product photo of a single fresh {item}, isolated on pure white seamless background, 
no surface visible, no plate, no table, no fabric, no props, floating, high key lighting, 
no shadows on background
```

**Result:** Second batch had clean white backgrounds with subtle product-photography shadows (acceptable quality).

## Error 3: Image filename mismatch (Airedale)

**Symptoms:** Page 3 showed empty placeholder box with text "airedale" instead of photo.

**Root cause:** Build script used "Airedale" as breed name → generated `airedale.png`. Image gen script used "Airedale Terrier" → saved `airedale_terrier.png`. HTML couldn't find the image.

**Fix:** Use identical breed names in both scripts. For this session: `cp airedale_terrier.png airedale.png`.

**Prevention:** After image generation, run a cross-check:
```python
for b, g in zip(build_names, gen_names):
    bf = b.lower().replace(' ', '_').replace("'", '') + '.png'
    gf = g.lower().replace(' ', '_').replace("'", '') + '.png'
    if bf != gf:
        print(f'MISMATCH: build expects {bf}, gen produces {gf}')
```

## Environment

- ComfyUI 0.22.0 on macOS (Apple Silicon MPS)
- Python 3.14 — asyncio bug prevents `comfy launch --background`
- Launch directly: `cd ~/Documents/comfy/ComfyUI && .venv/bin/python main.py --listen 127.0.0.1 --port 8188`
- SDXL base 1.0 checkpoint required
- Each image: ~40-50 seconds on MPS at 768×768, 20 steps
