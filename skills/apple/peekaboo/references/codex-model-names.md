# Codex Provider Model Names

Codex (OpenAI's ChatGPT backend) uses specific model slugs that differ from the standard OpenAI API model names. These were discovered by inspecting `hermes_cli/codex_models.py` in the Hermes Agent source.

## Supported Model Names

These are the Codex-compatible model slugs that work with the `openai-codex` provider:

- `gpt-5.4-mini`
- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.3-codex-spark`
- `gpt-5.2-codex`
- `gpt-5.1-codex-max`
- `gpt-5.1-codex-mini`

## Models That DO NOT Work

| Model name | Error |
|------------|-------|
| `deepseek-v4-flash` | "not supported when using Codex with a ChatGPT account" |
| `gpt-4o` | Same error |
| `gpt-4.1` | Same error |
| `gpt-4` | Same error |
| Empty/none | Falls back to config's `model.default` |

## Source

These were found in `hermes_cli/codex_models.py` in the Hermes Agent repo at `~/.hermes/hermes-agent/`. The file contains a `_CODEX_PLANS` array with valid model slugs and a `_FORWARD_COMPAT_TEMPLATE_MODELS` tuple for forward compatibility mapping.

The `openai-codex` provider resolves credentials via OAuth tokens stored in `~/.hermes/auth.json`, not via API keys. The auth flow uses ChatGPT's backend API at `https://chatgpt.com/backend-api/codex`.

## Config Impact

When the API server starts with a Codex model, it modifies `~/.hermes/config.yaml` to set `model.default` to the Codex slug. This breaks any concurrently-running DeepSeek server. Always restore with:

```bash
hermes config set model.default deepseek-v4-flash
```
