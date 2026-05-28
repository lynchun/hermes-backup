# Image Generation via OpenRouter Chat Completions

When the `image_generate` Hermes tool is unavailable (e.g. no FAL_KEY set),
you can generate images directly through the OpenRouter chat completions API
using image-capable models.

## Working Model

`openai/gpt-5-image-mini` — returns images in the `images` field of the
response message (NOT in `content`). Fast, good quality, ~$0.02-0.05/image.

## Recipe

```python
import json, urllib.request, os, base64

api_key = "..."  # OPENROUTER_API_KEY

body = {
    "model": "openai/gpt-5-image-mini",
    "messages": [{
        "role": "user",
        "content": "A professional botanical illustration of fresh spinach on white background. Scientific style. No text."
    }]
}

req = urllib.request.Request(
    'https://openrouter.ai/api/v1/chat/completions',
    data=json.dumps(body).encode(),
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost',
        'X-Title': 'Hermes Agent'}
)

resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
images = resp['choices'][0]['message'].get('images', [])

if images:
    img_url = images[0]['image_url']['url']  # data:image/png;base64,...
    header, b64 = img_url.split(',', 1)
    with open('output.png', 'wb') as f:
        f.write(base64.b64decode(b64))
```

## Failed Models

- **Gemini image models on OpenRouter** (`google/gemini-2.5-flash-image`,
  `google/gemini-3.1-flash-image-preview`): These models return `content: null`
  with encrypted `reasoning_details`. The image data is embedded in Google's
  C2PA provenance format which OpenRouter doesn't unwrap. DO NOT use these
  for image generation through OpenRouter.

## Batch Generation

For many images, run as a background process so the agent stays responsive:
```bash
terminal(command="python3 gen_images.py", background=True, notify_on_complete=True)
```

The script should skip already-downloaded images (check if file exists with
non-zero size) so interrupted runs can resume.
