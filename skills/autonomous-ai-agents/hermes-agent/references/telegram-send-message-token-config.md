# Telegram send_message Token Configuration

## Pitfall: Token must be in the RIGHT config section

The `send_message` tool and cron delivery read the Telegram bot token from
`config.platforms.telegram.token` — NOT from `os.environ['TELEGRAM_BOT_TOKEN']`
and NOT from the top-level `telegram.token` section.

### The bug
When the token is only in `.env` as `TELEGRAM_BOT_TOKEN`, the gateway's
Telegram adapter connects fine (it reads from env via `_apply_env_overrides()`),
but `send_message` fails with "You must pass the token."

`send_message` calls `load_gateway_config()` → `_apply_env_overrides()` which
reads from `os.environ` — but `os.environ` does NOT have the token because
`.env` is loaded by `load_dotenv()` into the Python process, and subprocesses
(or the agent's own tool handler context) may not inherit those env vars.

### The fix
Put the token under `platforms.telegram.token` in config.yaml:

```yaml
platforms:
  telegram:
    enabled: true
    token: "123456:ABC-DEF..."  # <-- HERE, not under top-level telegram:
```

NOT here (this doesn't work for send_message):
```yaml
telegram:           # top-level telegram settings section
  token: "..."      # <-- WRONG — send_message doesn't read this
```

### Why this works
`PlatformConfig.from_dict()` reads `token` from the platform data dict, which
is built from the `platforms:` section of config.yaml. The top-level `telegram:`
section is only used for bridging specific settings (require_mention,
allowed_chats, reactions, etc.) — NOT the token.

### Verifying the fix
```bash
# After adding token to platforms.telegram.token, restart gateway:
launchctl stop ai.hermes.gateway
launchctl start ai.hermes.gateway

# Then test:
send_message(target="telegram:CHAT_ID", message="test")
```
