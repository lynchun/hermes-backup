# ComfyUI Python 3.14 Launch Bug

## Symptom

`comfy launch --background` fails with:
```
RuntimeError: There is no current event loop in thread 'MainThread'.
```

The traceback shows `comfy_cli/command/launch.py:232` calling
`asyncio.get_event_loop()` which doesn't exist in Python 3.14
without a running event loop.

## Root Cause

Python 3.14 removed the implicit event loop creation that Python 3.12
and earlier provided. `asyncio.get_event_loop()` now raises RuntimeError
when called outside a running event loop.

## Fix

Launch ComfyUI directly with Python, bypassing comfy-cli's broken launcher:

```bash
cd ~/Documents/comfy/ComfyUI
.venv/bin/python main.py --listen 127.0.0.1 --port 8188
```

Run in background via Hermes:
```bash
terminal(
  command="cd ~/Documents/comfy/ComfyUI && .venv/bin/python main.py --listen 127.0.0.1 --port 8188",
  background=true,
  notify_on_complete=true
)
```

Verify it's running:
```bash
curl -s http://127.0.0.1:8188/system_stats
```

## Version Info

- Python: 3.14.2 (installed by uv for comfy-cli venv)
- comfy-cli: 1.10.3
- ComfyUI: installed via `uvx --from comfy-cli comfy install --m-series`
- macOS: Sequoia, Apple Silicon (M1 Max)
