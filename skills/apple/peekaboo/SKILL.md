---
name: peekaboo
description: "macOS desktop automation via Peekaboo — screen capture, UI element detection, mouse/keyboard interaction, and MCP server integration for Hermes."
version: 1.1.0
author: agent
platforms: [macos]
---

# Peekaboo — macOS Desktop Automation

Peekaboo is a macOS automation toolkit that captures screens, reads the accessibility tree, drives mouse/keyboard input, and ships an MCP server so AI agents can control the desktop.

## Installation

```bash
brew install steipete/tap/peekaboo
peekaboo --version     # Verify (tested: 3.1.2)
```

## Permissions

Peekaboo requires three macOS permissions. Grant via System Settings → Privacy & Security:

1. **Screen & System Audio Recording** — for screen captures
2. **Accessibility** — for mouse clicks, typing, UI interaction
3. **Event Synthesizing** — for synthetic input events

Verify with `peekaboo permissions`.

## MCP Server Registration

Register Peekaboo's MCP server with Hermes for tool access:

```bash
hermes mcp add peekaboo --command $(which peekaboo) --args mcp serve
# Accept "Enable all 25 tools?" when prompted
# Or: echo "Y" | hermes mcp add peekaboo --command $(which peekaboo) --args mcp serve
```

Reload in-session with `/reload-mcp`. A new session may be needed.

## Key Commands

| Task | Command |
|------|---------|
| Capture screenshot | `peekaboo image` (saves to /tmp) |
| See UI elements with JSON | `peekaboo see --json --mode frontmost` |
| See specific window | `peekaboo see --window-id N --json` |
| Click element | `peekaboo click --coord "x y"` or `peekaboo click --element-id elem_N` |
| Type text | `peekaboo type "Hello world"` |
| Press hotkey | `peekaboo hotkey cmd+space` |
| Scroll | `peekaboo scroll --direction down --amount 5` |
| List windows | `peekaboo list windows --app "Google Chrome"` |
| Capture with annotations | `peekaboo see --annotate --path /tmp/screen.png` |

## Finding UI Elements

Use `peekaboo see --json` to get structured element data. Key fields:
- `id` — stable element ID (use for `peekaboo click --element-id`)
- `bounds` — x, y, width, height
- `role_description` — "button", "text field", "tab", etc.
- `label` / `description` / `title` — human-readable text
- `is_actionable` — whether the element can be clicked/typed into

For window-specific targeting: `peekaboo list windows --app "AppName"` to get window IDs, then `peekaboo see --window-id N`.

### Practical Limitations

- **Complex web UIs (TradingView, Expedia) are impractical** via terminal-based Peekaboo interaction. Element discovery latency + multi-step navigation makes simple tasks take 10+ tool calls. **Workaround:** have the user navigate to the target page and share a screenshot or PDF, then analyse.
- **Bot-bypass advantage is real but slow** — Peekaboo controls real macOS UI, so it bypasses headless-browser detection. But element discovery/clicking speed makes it slower than a human. Best for: single-step actions (capture, click one button, read one value) not multi-step navigation flows.
- **`browser` tool (Chrome CDP)** appears in `peekaboo tools` list but `peekaboo browser --help` errors. Use through MCP tool interface, not CLI.
- **OCR fallback is essential** for web-rendered content (TradingView charts, canvas elements). Peekaboo's accessibility tree may not capture all rendered text. Use `tesseract` on captured screenshots.
- **User stopped complex navigation** during a TradingView session because Peekaboo was too slow. Keep interactions to 2-3 steps maximum.
- **Annotated screenshots** (`--annotate`) generate two files: raw capture + annotated version (element numbers overlaid).

## Hermes API Server (Open WebUI Integration)

The Hermes API server provides an OpenAI-compatible endpoint so Open WebUI can chat with Hermes Agent.

### Critical: Provider Selection

**Without `HERMES_INFERENCE_PROVIDER=deepseek`**, the API server defaults to `openai-codex` which rejects model names like `deepseek-v4-flash` or `gpt-4o`:
```
"The 'deepseek-v4-flash' model is not supported when using Codex with a ChatGPT account."
```

Always set `HERMES_INFERENCE_PROVIDER=deepseek` when starting for DeepSeek use.

### Standalone Start

```bash
# Kill any existing process first
lsof -ti :8642 | xargs kill 2>/dev/null

cd ~/.hermes/hermes-agent && \
  HERMES_INFERENCE_PROVIDER=deepseek \
  API_SERVER_PORT=8642 \
  API_SERVER_HOST=0.0.0.0 \
  API_SERVER_KEY=local-dev \
  API_SERVER_MODEL_NAME="Epictetus" \
  DEEPSEEK_API_KEY=sk-xxx \
  ~/.hermes/hermes-agent/venv/bin/python3 scripts/hermes-api-server.py &
```

### Model Name in Open WebUI

Controlled by `API_SERVER_MODEL_NAME`. User now prefers consistent naming with backend:

| Env Value | Shows in Open WebUI |
|-----------|-------------------|
| `API_SERVER_MODEL_NAME="Epictetus (DeepSeek)"` | `Epictetus (DeepSeek)` ✓ (current preference) |
| `API_SERVER_MODEL_NAME="Epictetus (Codex)"` | `Epictetus (Codex)` ✓ (vision-capable option) |
| `API_SERVER_MODEL_NAME="Epictetus"` | `Epictetus` — old style, user found confusing |

### Open WebUI Connection

In Open WebUI → Settings → Connections → Direct Connections, add:
- **URL:** `http://host.docker.internal:8642/v1` (Docker) or `http://localhost:8642/v1`
- **API Key:** `local-dev`

### Prerequisites

- `pip3 install aiohttp` — required for the API server
- Verify: `python3 -c "import aiohttp; print('ok')"`
- Binding to 0.0.0.0 requires `API_SERVER_KEY`
- The port number in `API_SERVER_PORT` must match what Open WebUI connects to

### Codex as Backend (Working with Correct Model Name)

Codex can serve as a Hermes backend with vision capability. The API server requires a Codex-compatible model name:

```bash
# Codex-specific model names that work:
# gpt-5.4-mini, gpt-5.4, gpt-5.3-codex, gpt-5.3-codex-spark
# gpt-5.2-codex, gpt-5.1-codex-max, gpt-5.1-codex-mini

cd ~/.hermes/hermes-agent && \
  API_SERVER_MODEL="gpt-5.3-codex" \
  HERMES_INFERENCE_PROVIDER=openai-codex \
  API_SERVER_PORT=8643 \
  API_SERVER_HOST=0.0.0.0 \
  API_SERVER_KEY=local-dev \
  API_SERVER_MODEL_NAME="Epictetus (Codex)" \
  ~/.hermes/hermes-agent/venv/bin/python3 scripts/hermes-api-server.py
```

**CRITICAL:** The script modifies `~/.hermes/config.yaml` to set `model.default` to the Codex model name. This breaks the DeepSeek server. **Always restore config after Codex server exits** (the script has cleanup code for this, but if it's killed uncleanly, run `hermes config set model.default deepseek-v4-flash`).

**Open WebUI connection** needs a separate Direct Connection:
- URL: `http://host.docker.internal:8643/v1`
- Key: `local-dev`

**Model names that DO NOT work with Codex:**
- `deepseek-v4-flash` — returns: `"The 'deepseek-v4-flash' model is not supported when using Codex"`
- `gpt-4o` — same error
- `gpt-4.1` — not supported

### Scripts

- `scripts/hermes-api-server.py` — standalone launcher with env-var-driven provider selection.

## Use Cases

1. **Flight/price comparison** — Navigate Expedia, Skyscanner, Kayak without bot detection (bypasses headless detection via real macOS UI)
2. **Desktop automation** — Click buttons, fill forms, read from any app
3. **Visual debugging** — See what's on screen when UI element detection doesn't return expected results
4. **Browser control** — The `browser` tool (Chrome CDP) offers alternative web control

## Reference

- Homepage: https://peekaboo.sh/
- GitHub: https://github.com/openclaw/Peekaboo
- MCP tools available: click, swipe, dialog, dock, scroll, analyze, set_value, move, perform_action, clipboard, app, permissions, space, menu, agent, sleep, drag, image, paste, see, hotkey, list, window, browser, type

## Config Conflict (Dual API Servers)

See `references/api-server-config-conflict.md` for the shared-config.yaml issue that prevents running both DeepSeek and Codex API servers simultaneously.
