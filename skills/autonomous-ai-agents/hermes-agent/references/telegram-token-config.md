# Telegram Platform Token Configuration

## The Token Must Be Under `platforms.telegram.token`

The `send_message` tool and cron delivery system read the bot token from `config.platforms[Platform.TELEGRAM].token`, which maps to the YAML:

```yaml
platforms:
  telegram:
    enabled: true
    token: "123456:ABC-DEF..."   # ← HERE, not top-level
```

## Common Misconfigurations

**❌ Token only in `.env` (`TELEGRAM_BOT_TOKEN`):** The gateway startup calls `_apply_env_overrides()` which reads from `os.environ`. But the `send_message` tool's `load_gateway_config()` call may run in a context where `.env` variables aren't exported. Result: gateway connects, but `send_message` fails with "You must pass the token."

**❌ Token under top-level `telegram:` section:** The top-level `telegram:` section (with `allowed_chats`, `reactions`, etc.) is bridged into env vars by `load_gateway_config()` but ONLY for specific fields (`require_mention`, `guest_mode`, `allowed_chats`, etc.) — NOT for `token`. The `token` field from the top-level section is never copied into the platform config.

**✅ Token under `platforms.telegram.token`:** This is the canonical location. Both the gateway adapter and the `send_message` tool read from here.

## Debugging Checklist

1. Check token location: `grep -A5 'platforms:' ~/.hermes/config.yaml | grep -A3 telegram`
2. Verify token works directly: `curl -s "https://api.telegram.org/bot$TOKEN/sendMessage" -d "chat_id=USER_ID" -d "text=test"`
3. Restart gateway after config change: `launchctl stop ai.hermes.gateway; sleep 2; launchctl start ai.hermes.gateway`
4. Test `send_message`: `send_message(target="telegram:USER_ID", message="test")`

## Same Pattern for Other Platforms

Discord, Slack, Matrix, Mattermost tokens follow the same rule — they MUST be under `platforms.<name>.token`, not just in `.env` or under a top-level `<name>:` section.
