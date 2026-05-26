# OpenRouter Vision for Cover Art Analysis

Configured for Lyndon's system to analyse album art and promo video frames
via vision-capable models when the primary model (DeepSeek) lacks vision.

## Setup

```bash
# 1. Get API key from https://openrouter.ai/keys
# 2. Add to ~/.hermes/.env:
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> ~/.hermes/.env

# 3. Configure as provider (optional — can use API directly as above)
hermes config set model.provider openrouter
hermes config set model.default "google/gemini-3-flash-preview"
```

## Usage for Cover Art / Video Frame Analysis

Use direct curl to OpenAI-compatible endpoint (works regardless of current provider):

```python
import subprocess, json, base64

API_KEY = "sk-or-v1-..."  # from .env
with open("/tmp/image.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

body = json.dumps({
    "model": "google/gemini-3-flash-preview",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image in detail..."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        ]
    }],
    "max_tokens": 500
})

result = subprocess.run([
    "curl", "-s", "https://openrouter.ai/api/v1/chat/completions",
    "-H", f"Authorization: Bearer {API_KEY}",
    "-H", "Content-Type: application/json",
    "-d", body
], capture_output=True, text=True)

data = json.loads(result.stdout)
description = data["choices"][0]["message"]["content"]
```

## Recommended Vision Models (cheap, fast)

| Model | Cost | Speed | Quality |
|-------|------|-------|---------|
| google/gemini-3-flash-preview | ~$0.10/M | Fast | Good for cover art analysis |
| google/gemini-2.5-flash-image | ~$0.15/M | Fast | Good balance |
| anthropic/claude-sonnet-4 | ~$3/M | Moderate | Best quality for complex visuals |

## Pre-processing

Always convert to JPEG and resize before sending:

```bash
sips -s format jpeg -Z 800 large_image.png --out /tmp/analysable.jpg
```

Max dimension of 800px keeps tokens low while preserving enough detail for
colour/typography/layout analysis.
