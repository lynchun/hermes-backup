# Hermes API Server — Open WebUI Integration

Connecting Open WebUI (or any OpenAI-compatible client) to Hermes Agent via the built-in API server.

## Quick Setup

### Prerequisites
- Open WebUI running (Docker container or pip install)
- `aiohttp` installed in Hermes venv

### Steps

**1. Enable the api_server platform in config.yaml**

Add at the TOP level of `~/.hermes/config.yaml` (NOT nested under `gateway:`):

```yaml
platforms:
  api_server:
    enabled: true
```

**2. Install dependency**

```bash
pip3 install aiohttp
# Also need it in Hermes venv (auto-detected from system)
```

**3. Start the API server via the standalone script**

The API server script is saved in the skill's `scripts/` directory:

```bash
cp ~/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/api_server.py /tmp/
```

Then run with the desired provider:

```bash
cd ~/.hermes/hermes-agent

# DeepSeek backend
HERMES_INFERENCE_PROVIDER=deepseek API_SERVER_MODEL_NAME="Epictetus" \
  API_SERVER_PORT=8642 API_SERVER_HOST=0.0.0.0 API_SERVER_KEY=local-dev \
  ~/.hermes/hermes-agent/venv/bin/python3 /tmp/api_server.py

# Codex backend (requires API_SERVER_MODEL to set correct model in config)
HERMES_INFERENCE_PROVIDER=openai-codex API_SERVER_MODEL="gpt-5.3-codex" \
  API_SERVER_PORT=8643 API_SERVER_MODEL_NAME="Epictetus (Codex)" \
  API_SERVER_HOST=0.0.0.0 API_SERVER_KEY=local-dev \
  ~/.hermes/hermes-agent/venv/bin/python3 /tmp/api_server.py
```

**4. Add to Open WebUI**

Settings → Connections → Direct Connections → + → enter:
- **URL:** `http://host.docker.internal:8642/v1`
- **API Key:** `local-dev`

**5. Test the connection**

```bash
curl -s http://localhost:8642/v1/models -H "Authorization: Bearer local-dev"
# Should return: {"object":"list","data":[{"id":"Epictetus",...}]}

curl -s http://localhost:8642/v1/chat/completions \
  -H "Authorization: Bearer local-dev" \
  -H "Content-Type: application/json" \
  -d '{"model":"Epictetus","messages":[{"role":"user","content":"hello"}]}'
```

## Pitfalls

### API server binding to 0.0.0.0
Binding to all interfaces requires `API_SERVER_KEY` to be set. Without it, the server refuses to start:
```
[Api_Server] Refusing to start: binding to 0.0.0.0 requires API_SERVER_KEY.
```

### Provider resolution
The API server uses `resolve_runtime_provider()` which reads `HERMES_INFERENCE_PROVIDER` env var. If this isn't set, it may pick up `openai-codex` as the default provider and fail with:
```
The 'deepseek-v4-flash' model is not supported when using Codex with a ChatGPT account.
```
Fix: Set `HERMES_INFERENCE_PROVIDER=deepseek` in the environment.

### Model name
The advertised model name (shown in Open WebUI) is controlled by `API_SERVER_MODEL_NAME`. If not set, falls back to the active profile name, then `"hermes-agent"`.

```bash
API_SERVER_MODEL_NAME="Epictetus"
```

Display names should be clean — no backend clutter. Use just `"Epictetus"` or `"Epictetus (Codex)"`, never the underlying model name.

### Port conflicts
Kill old processes before starting a new one:
```bash
kill $(lsof -i :8642 -P | grep LISTEN | awk '{print $2}') 2>/dev/null
```

### Gateway integration (alternative)
The platform can also be configured via the gateway service, but getting the config format right is complex. The standalone background process approach above is more reliable. If using the gateway:
- Top-level `platforms:` key (NOT `gateway.platforms`)
- Requires `aiohttp` in the Hermes venv
- Requires `GATEWAY_ALLOW_ALL_USERS=true` or allowlist config
- API server port from `API_SERVER_PORT` env var or `gateway.api_server.port`

## Open WebUI + Docker

When Open WebUI runs in Docker, use `host.docker.internal` instead of `localhost` for the URL:
- `http://host.docker.internal:8642/v1` (inside container → host)
- `http://localhost:8642/v1` (on host directly)

## Multi-model setup

Run multiple API servers on different ports to expose different backends:

| Port | Env vars | Model name |
|------|----------|------------|
| 8642 | `HERMES_INFERENCE_PROVIDER=deepseek` | Epictetus (DeepSeek) |
| 8643 | `HERMES_INFERENCE_PROVIDER=openai-codex`, `API_SERVER_MODEL=gpt-5.3-codex` | Epictetus (Codex) |

### CRITICAL: Config Conflict — Only One API Server at a Time

**Two Hermes API servers cannot share the same `config.yaml` simultaneously** because `_resolve_gateway_model()` reads `model.default` on every new request. The script writes the desired model to config.yaml at startup, and only one model name can be in the file at once.

When you switch between them:
- The second server overwrites `model.default` in config.yaml
- The first server then reads the wrong model on its next request and fails

**Workaround:** Keep only one API server running at a time. Kill the current one before starting the other:

```bash
kill $(lsof -i :8642 -P | grep LISTEN | awk '{print $2}') 2>/dev/null
kill $(lsof -i :8643 -P | grep LISTEN | awk '{print $2}') 2>/dev/null
# Then start the desired one
```

### Codex Provider Model Names

When using `HERMES_INFERENCE_PROVIDER=openai-codex`, set `API_SERVER_MODEL` to one of these (from `hermes_cli/codex_models.py`):

- `gpt-5.4-mini`
- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.3-codex-spark` (ChatGPT Pro only)
- `gpt-5.2-codex`
- `gpt-5.1-codex-max`
- `gpt-5.1-codex-mini`

Codex does NOT accept non-Codex model names like `deepseek-v4-flash` or `gpt-4o`. The error `The 'X' model is not supported when using Codex with a ChatGPT account` means the model name is wrong for the Codex provider.

### Server Process Management

```bash
# Find running API server on a port
lsof -i :8642 -P | grep LISTEN

# Kill by PID
kill <PID>

# Kill all Hermes API servers
kill $(lsof -i :8642 -P | grep LISTEN | awk '{print $2}') 2>/dev/null
kill $(lsof -i :8643 -P | grep LISTEN | awk '{print $2}') 2>/dev/null
```

### Config Modification Side Effect

The API server script (`api_server.py`) modifies `~/.hermes/config.yaml` at startup (changing `model.default` to the value of `API_SERVER_MODEL`). On clean shutdown, it restores the old value. On unclean shutdown (kill -9, timeout, crash), the config is left with the modified value.

**After an unclean shutdown of a Codex server,** always restore the DeepSeek model:
```bash
hermes config set model.default deepseek-v4-flash
```

### Open WebUI Model Name Refresh

When the API server advertises a new model name, Open WebUI caches the model list. The user must click the model selector → refresh icon to see the new name.

## Env Var Reference

| Env var | Purpose | Example |
|---------|---------|---------|
| `HERMES_INFERENCE_PROVIDER` | Backend provider | `deepseek`, `openai-codex` |
| `API_SERVER_MODEL` | Model name for config override | `deepseek-v4-flash`, `gpt-5.3-codex` |
| `API_SERVER_MODEL_NAME` | Display name in Open WebUI | `Epictetus`, `Epictetus (Codex)` |
| `API_SERVER_PORT` | Listen port | `8642`, `8643` |
| `API_SERVER_HOST` | Bind address | `127.0.0.1`, `0.0.0.0` |
| `API_SERVER_KEY` | API key for auth | `local-dev` |
