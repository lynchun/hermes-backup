# Standalone Hermes API Server

For running Hermes Agent behind Open WebUI, Cursor, or any OpenAI-compatible
client without going through the full gateway (>20k lines of messaging-platform
infrastructure that is unused for local API-only setups).

## When to run standalone instead of via `hermes gateway`

| Situation | Use |
|-----------|-----|
| You want a lightweight API server for a single client | Standalone |
| You need multiple API servers on different ports (e.g. DeepSeek + Codex) | Standalone (one per port) |
| You need messaging platforms (Telegram, Discord, etc.) | Gateway |
| The gateway's `api_server` platform won't activate due to config issues | Standalone |

## Quick Start

Create a Python script (see `/tmp/hermes_api_server.py` on Lyndon's Mac):

```python
#!/usr/bin/env python3
"""Start Hermes API server standalone"""
import os, sys, asyncio
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))
os.environ['HERMES_INFERENCE_PROVIDER'] = os.environ.get('HERMES_INFERENCE_PROVIDER', 'deepseek')
os.environ['API_SERVER_PORT'] = os.environ.get('API_SERVER_PORT', '8642')
os.environ['API_SERVER_HOST'] = os.environ.get('API_SERVER_HOST', '0.0.0.0')
os.environ['API_SERVER_KEY'] = os.environ.get('API_SERVER_KEY', 'local-dev')
os.environ['API_SERVER_MODEL_NAME'] = os.environ.get('API_SERVER_MODEL_NAME', 'Epictetus')

from gateway.config import PlatformConfig

async def main():
    config = PlatformConfig(enabled=True)
    from gateway.platforms.api_server import APIServerAdapter
    adapter = APIServerAdapter(config)
    success = await adapter.connect()
    if success:
        while True:
            await asyncio.sleep(3600)
    else:
        print('Failed to start')

if __name__ == '__main__':
    asyncio.run(main())
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `API_SERVER_PORT` | 8642 | Listening port |
| `API_SERVER_HOST` | 0.0.0.0 | Listening host |
| `API_SERVER_KEY` | (empty) | API key for auth. **Required** when binding to 0.0.0.0 |
| `API_SERVER_MODEL_NAME` | "hermes-agent" | Name advertised in /v1/models |
| `HERMES_INFERENCE_PROVIDER` | deepseek | Provider to use (deepseek, openai-codex, etc.) |

## Provider-Specific Notes

### DeepSeek
```bash
HERMES_INFERENCE_PROVIDER=deepseek \
DEEPSEEK_API_KEY=sk-xxx \
API_SERVER_PORT=8642 \
API_SERVER_MODEL_NAME="Epictetus (DeepSeek)" \
python3 script.py
```

### Codex (OpenAI via ChatGPT OAuth)
```bash
HERMES_INFERENCE_PROVIDER=openai-codex \
API_SERVER_PORT=8643 \
API_SERVER_MODEL_NAME="Epictetus (Codex)" \
python3 script.py
```

**Codex model name limitation:** The `API_SERVER_MODEL_NAME` only changes the
advertised name in `/v1/models`. The actual model used for inference is read
from `model.default` in config.yaml (via `_resolve_gateway_model()`). Codex
does not support the `deepseek-v4-flash` model. To use Codex backend, you
must either:
1. Set `model.default` to a Codex-compatible model (e.g. `gpt-5.3-codex`)
2. Accept that changing config.yaml affects ALL API servers sharing it

### Known Limitation: Shared Config.yaml

Multiple API servers share the same `~/.hermes/config.yaml`. When one server
starts, it may modify `model.default` to its own model name, breaking the
other server. The long-term fix is a per-server config override, but currently
the `_resolve_gateway_model()` function reads the global config.

**Workaround:** Only one API server can run at a time unless both servers
use the same model name.
