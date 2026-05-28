#!/usr/bin/env python3
"""Generate botanical-style images for reference sheets via OpenRouter GPT-5-image-mini.
Usage: python3 gen_ref_images.py <data.json> <output_dir>
"""
import json, urllib.request, os, base64, re, sys, time

data_file = sys.argv[1]
out_dir = sys.argv[2]

api_key = os.popen("grep OPENROUTER_API_KEY ~/.hermes/.env | cut -d= -f2").read().strip()
os.makedirs(out_dir, exist_ok=True)

with open(data_file) as f:
    items = [v['en'] for v in json.load(f)]

done = fail = 0
for i, item in enumerate(items):
    fname = os.path.join(out_dir, f"{item.replace(' ', '_')}.png")
    if os.path.exists(fname) and os.path.getsize(fname) > 1000:
        print(f"[{i+1}/{len(items)}] SKIP {item} (exists)")
        done += 1
        continue

    body = {
        "model": "openai/gpt-5-image-mini",
        "messages": [{"role": "user", "content": f"A professional botanical illustration of fresh {item} on a pure white background. Scientific reference style, detailed, natural lighting. No text, no labels, no borders. Square format."}]
    }
    
    try:
        req = urllib.request.Request(
            'https://openrouter.ai/api/v1/chat/completions',
            data=json.dumps(body).encode(),
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'HTTP-Referer': 'http://localhost', 'X-Title': 'Hermes Agent'}
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        images = resp['choices'][0]['message'].get('images', [])
        
        if images and images[0]['image_url']['url'].startswith('data:'):
            header, b64 = images[0]['image_url']['url'].split(',', 1)
            m = re.search(r'image/(\w+)', header)
            ext = m.group(1) if m else 'png'
            with open(fname, 'wb') as f:
                f.write(base64.b64decode(b64))
            print(f"[{i+1}/{len(items)}] OK {item} ({os.path.getsize(fname)} bytes)")
            done += 1
        else:
            print(f"[{i+1}/{len(items)}] FAIL {item} — no image")
            fail += 1
    except Exception as e:
        print(f"[{i+1}/{len(items)}] ERROR {item}: {e}")
        fail += 1
        time.sleep(2)

print(f"\nDONE: {done} ok, {fail} fail, {done+fail}/{len(items)}")
