# Proven SDXL Workflow for MPS (macOS Apple Silicon)

This template is confirmed working on ComfyUI 0.22.0 with MPS backend (M1 Max 64GB).
The skill's built-in `sdxl_txt2img.json` (dpmpp_2m/karras at 1024×1024) returns HTTP 500 on MPS.

## Python submission template

```python
import requests

workflow = {
    "3": {"class_type": "KSampler", "inputs": {
        "seed": 42, "steps": 20, "cfg": 7,
        "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
        "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]
    }},
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {
        "ckpt_name": "sd_xl_base_1.0.safetensors"
    }},
    "5": {"class_type": "EmptyLatentImage", "inputs": {
        "width": 768, "height": 768, "batch_size": 1
    }},
    "6": {"class_type": "CLIPTextEncode", "inputs": {
        "text": "YOUR PROMPT HERE", "clip": ["4", 1]
    }},
    "7": {"class_type": "CLIPTextEncode", "inputs": {
        "text": "ugly, blurry, low quality, deformed, watermark, text, label, multiple objects",
        "clip": ["4", 1]
    }},
    "8": {"class_type": "VAEDecode", "inputs": {
        "samples": ["3", 0], "vae": ["4", 2]
    }},
    "9": {"class_type": "SaveImage", "inputs": {
        "filename_prefix": "output", "images": ["8", 0]
    }},
}

resp = requests.post("http://127.0.0.1:8188/api/prompt", json={"prompt": workflow})
pid = resp.json()["prompt_id"]

# Poll for completion
import time
while True:
    time.sleep(1)
    hist = requests.get(f"http://127.0.0.1:8188/history/{pid}").json()
    if pid in hist:
        break
```

## Prompt templates

**Product photography (fruits, vegetables, objects):**
```
studio product photo of a single fresh {item}, isolated on pure white seamless background, no surface visible, no plate, no table, no fabric, no props, floating, high key lighting, no shadows on background
```

**Pet/animal photography (dogs, cats, etc.):**
```
studio photograph of a purebred {breed} dog, full body, standing on pure white seamless background, professional pet photography, isolated, no collar, no props, high key lighting, no shadows on background
```

## Timing
- ~45s per 768×768 image on M1 Max MPS
- Deterministic output with fixed seed: `abs(hash(item_name)) % 2147483647`
