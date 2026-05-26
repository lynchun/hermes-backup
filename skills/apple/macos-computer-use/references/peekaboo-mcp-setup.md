# Peekaboo MCP Integration (macOS Desktop Automation)

Peekaboo (https://peekaboo.sh) is a macOS automation toolkit installed via
Homebrew: `brew install steipete/tap/peekaboo`. It exposes 25 tools (click,
type, see, capture, browser, dock, window, scroll, drag, etc.) through an
MCP server.

## Registration

```bash
# Non-interactive (recommended for agent use):
echo "Y" | hermes mcp add peekaboo --command "$(which peekaboo)" --args mcp serve

# Interactive:
hermes mcp add peekaboo --command "$(which peekaboo)" --args mcp serve
# Then answer Y when prompted to enable all 25 tools
```

## Reload

After `hermes mcp add peekaboo`, run `/reload-mcp` in the active session
or start a new session for the tools to appear.

## Permission Requirements (manual grant)

Peekaboo needs two macOS permissions:

1. **Screen Recording** — System Settings → Privacy → Screen & System Audio
   Recording → add Terminal.app
2. **Accessibility** — System Settings → Privacy → Accessibility → add
   Terminal.app

Without these, `peekaboo permissions` shows "Not Granted" and tool calls
will fail.

## Tool Categories (25 total)

| Category | Tools |
|----------|-------|
| Capture/Vision | `see`, `image`, `analyze` |
| Input | `click`, `type`, `hotkey`, `press`, `paste`, `scroll`, `drag`, `move` |
| UI | `menu`, `dialog`, `window`, `dock`, `space`, `app`, `list` |
| System | `permissions`, `clipboard`, `set_value`, `perform_action`, `sleep` |
| Agent | `agent` (built-in AI plan/act loop) |
| Browser | `browser` (Chrome DevTools Protocol) |

## Use Cases for This User

- **Travel site searching** — Expedia, Skyscanner, Kayak all block headless
  browsers. Peekaboo controls the real macOS browser = no bot detection.
- **Any web research** where sites block automation
- **Desktop UI interaction** with native macOS apps

## Data Privacy

Peekaboo captures visible screen content only. Masked password fields
appear as "••••••". However, anything Peekaboo sees on screen that gets
processed goes through whatever AI model is running (DeepSeek, etc.).

For private client data: use only through the `local` Hermes profile
(Llama 3.1 8B via Ollama), NOT while on DeepSeek.

## Reload After Registration

After `hermes mcp add peekaboo`, run `/reload-mcp` in the active session
or start a new session for the tools to appear.

## Process Management

When killing Peekaboo servers or other background processes, the killed
process may produce output notifications (stale log traces) that show up
as `[IMPORTANT: Background process X completed]` to the user. These are
harmless — they're just the process's shutdown sequence flushing to the
terminal. The user may find these noisy; minimise unnecessary kills.

When running Peekaboo alongside the Hermes API server (Open WebUI),
killing a process can also leave stale listeners on a port:
```bash
lsof -i :8642 -P | grep LISTEN   # Check port
kill <PID>                        # If something's still listening
```

## Limitations

- **Complex multi-step navigation is slow** — each step (find element,
  click, wait for page, re-capture) is a tool call. A 5-step search
  on Expedia takes 10+ calls and 30-60 seconds.
- **Not viable for autonomous comparison shopping** — the user finds
  better deals manually in less time.
- **Best for single-step captures** — take a screenshot of a page and
  OCR it, or click one button.
- **Element IDs stale after page navigation** — re-capture before
  clicking after any page load.
