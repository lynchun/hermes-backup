# OpenRouter Image Generation (ComfyUI Backup)

When ComfyUI is unavailable (Python 3.14 BrokenPipeError, GPU OOM, etc.), use
OpenRouter's `openai/gpt-5-image-mini` model for batch image generation.

## Quick Recipe

```python
import json, urllib.request, os, base64, re

# Read API key from Hermes .env
env = open(os.path.expanduser("~/.hermes/.env")).read()
API_KEY = re.search(r'OPENROUTER_API_KEY=(.+)', env).group(1).strip().strip('"')

prompt = "studio photograph of a single squirrel, isolated on pure white seamless background, professional wildlife photography, no props"

body = {
    "model": "openai/gpt-5-image-mini",
    "messages": [{"role": "user", "content": prompt}]
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Hermes Agent"
    }
)

resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
images = resp["choices"][0]["message"].get("images", [])

if images:
    img_url = images[0]["image_url"]["url"]  # data:image/png;base64,...
    _, b64 = img_url.split(",", 1)
    with open("output.png", "wb") as f:
        f.write(base64.b64decode(b64))
```

## Parameters
- **Model:** `openai/gpt-5-image-mini` (only confirmed working model via OR)
- **Cost:** ~$0.02-0.05/image
- **Speed:** ~15-25 sec/image (API + rate limiting)
- **Quality:** Good product-photography style, clean white backgrounds
- **Rate limit:** Add 1-second sleep between requests to avoid 429s

## Prompt Templates (per category)

| Category | Prompt |
|----------|--------|
| Animals | `studio photograph of a single {name}, isolated on pure white seamless background, professional wildlife photography, no props, no collar` |
| Trees | `studio photograph of a {name} tree, isolated on pure white seamless background, professional botanical photography, no ground, no shadows` |
| Transport | `studio product photo of a single {name}, isolated on pure white seamless background, no surface visible, professional product photography` |
| Instruments | `studio product photo of a single {name}, isolated on pure white seamless background, no surface visible, professional product photography` |
| Food/Plants | `studio product photo of a single fresh {name}, isolated on pure white seamless background, no surface visible, no props, high key lighting` |

## Failed Models (DO NOT USE)
- **Gemini image models on OpenRouter** (`google/gemini-2.5-flash-image`, etc.): Return `content: null` with encrypted C2PA provenance data. Images are embedded in Google's format which OpenRouter doesn't unwrap.

## Batch Generation Script
Save as `gen_images_or.py`, reads assessment data files, skips existing images > 1KB, generates the rest. Runs in background: `terminal(command="python3 gen_images_or.py", background=True, notify_on_complete=True)`.
