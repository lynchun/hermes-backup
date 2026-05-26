# Hermes API Server — Config.yaml Sharing Conflict

## The Problem

The Hermes API server script (`scripts/hermes-api-server.py`) creates an AIAgent for each request. The AIAgent reads `model.default` from `~/.hermes/config.yaml`. This means **two API servers cannot coexist on different ports** — they share the same config file and whichever model was set last will be used by both.

### How It Manifests

1. Start DeepSeek server on :8642 → config sets `model.default: deepseek-v4-flash` → works
2. Start Codex server on :8643 → config sets `model.default: gpt-5.3-codex` → Codex works
3. DeepSeek server on :8642 now reads `gpt-5.3-codex` → FAILS with:
   ```
   "The 'gpt-5.3-codex' model is not supported when using openai-codex with a ChatGPT account."
   ```
   (Or vice versa — Codex fails when config says `deepseek-v4-flash`)

### Why

The API server's `_resolve_gateway_model()` function reads from the shared `config.yaml`:

```python
# gateway/platforms/api_server.py
model = _resolve_gateway_model()
```

And `_resolve_gateway_model()`:

```python
# gateway/run.py
def _resolve_gateway_model(config=None):
    cfg = config if config is not None else _load_gateway_config()
    return cfg.get("model", {}).get("default", "")
```

Since both API server processes read from the same `config.yaml`, they cannot have different model defaults.

## Possible Fixes (Not Yet Implemented)

### Option A: Separate Config Files
Create a wrapper that passes a different config path to `_load_gateway_config()` — requires modifying Hermes source code.

### Option B: Model Override Parameter
The AIAgent constructor accepts a `model=` parameter. If the API server could pass a model override without touching config.yaml, both servers could coexist. Would require adding an env var like `HERMES_OVERRIDE_MODEL` that bypasses config read.

### Option C: Accept Single-Server Limitation
Only run one API server at a time. Use a helper script to swap:
```bash
alias switch-to-deepseek='lsof -ti :8642 | xargs kill 2>/dev/null; hermes config set model.default deepseek-v4-flash'
alias switch-to-codex='lsof -ti :8643 | xargs kill 2>/dev/null; hermes config set model.default gpt-5.3-codex'
```

### Option D: Use OpenAI API Key Instead
Add GPT-4o as a native connection in Open WebUI (not via Hermes API server). Open WebUI connects directly to `https://api.openai.com/v1` — no config sharing issue. Requires an OpenAI API key.

## Current Best Practice

Per user preference, run **one API server at a time**:
- **DeepSeek** (port 8642) for general use
- **Codex** (port 8643) when vision/images are needed, then kill it and restore DeepSeek config

The user does not need both simultaneously. The DeepSeek server handles 95% of daily use.
