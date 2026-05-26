# Multi-Profile Model Switching for Hermes

How to set up and switch between multiple Hermes profiles, each with a different model/provider.

## Profiles Created

| Profile | Model | Provider | When to use |
|---------|-------|----------|-------------|
| `default` | deepseek-v4-flash | deepseek | General chat, research, web |
| `local` | llama3.1:8b | local Ollama | Client files, private data |

## Commands

```bash
# Use local profile
local chat

# Use default profile
hermes

# Quick one-off query on local
hermes --profile local chat -q "question"

# Switch sticky default
hermes profile use <name>
```

## Local Profile Details

The `local` profile was created with:
```bash
hermes profile create local --clone-from default
hermes config set --profile local model.default llama3.1:8b
hermes config set --profile local model.provider ollama_local
hermes config set --profile local model.base_url http://localhost:11434/v1
```

A wrapper script `local` is at `~/.local/bin/local`.

## Performance Notes

Local models are slow in Hermes due to context overhead (tool schemas, system prompts, conversation management). For quick private queries, use `ollama` directly:

```bash
cat document.txt | ollama run llama3.1:8b "Summarise this"
```

## Adding More Profiles

```bash
hermes profile create <name> --clone-from default
# Then configure the model/provider
```

## Data Privacy

Client files (AAPs, SoAs) must NEVER be processed on cloud models. The `local` profile ensures everything runs on your Mac.
