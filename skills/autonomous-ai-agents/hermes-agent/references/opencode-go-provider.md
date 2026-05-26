# OpenCode Go Provider

OpenCode Go (`opencode-go`) is a provider in Hermes that routes through
`https://opencode.ai/zen/go/v1`. It offers 15 models including DeepSeek V4
Flash and Pro.

## Key Finding
The `/v1/models` endpoint is public (no auth needed). Inference requires
`OPENCODE_GO_API_KEY` in `.env`. Whether usage is free or paid depends on
OpenCode's pricing model — verify before switching.

## Available Models (as of May 2026)
```
deepseek-v4-pro        deepseek-v4-flash     glm-5.1
glm-5                  kimi-k2.6             kimi-k2.5
minimax-m2.7           minimax-m2.5          qwen3.6-plus
qwen3.5-plus           mimo-v2-pro           mimo-v2-omni
mimo-v2.5-pro          mimo-v2.5             hy3-preview
```

## Setup
```bash
# Add API key
echo "OPENCODE_GO_API_KEY=your-key" >> ~/.hermes/.env

# Switch provider
hermes config set model.provider opencode-go
hermes config set model.default deepseek-v4-flash
```

## Provider Details
- Plugin: `plugins/model-providers/opencode-zen/__init__.py`
- Aliases: `opencode_go`, `go`, `opencode-go-sub`
- Base URL: `https://opencode.ai/zen/go/v1`
- Default aux model: `glm-5`
- API mode: chat_completions for most models, anthropic_messages for MiniMax
