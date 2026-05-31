# Security Sweep Cron Job

Weekly automated macOS security audit using Codex (GPT-5) for threat reasoning. Read-only, non-invasive.

## Prompt Template

```
Run a non-invasive macOS security audit. Read-only. Do NOT install, modify, or change anything.

Check and report findings with severity (CRITICAL/HIGH/MEDIUM/LOW):

1. Launch daemons and agents — list system and user daemons, check if executable paths are user-writable or unsigned using codesign. Flag anything suspicious or new.

2. Firewall and network — check firewall state, list listening TCP ports. Flag any non-localhost listeners.

3. System integrity — check SIP, Gatekeeper, software update status, FileVault encryption status.

4. Remote access — check if remote login is enabled, verify SSH directory permissions, check for unexpected access vectors.

5. Persistence — check crontabs, login items, kernel extensions (non-Apple).

6. Applications — scan Applications folder for unsigned or recently added apps.

7. Services — check Docker, Ollama, and any other running services for known exposure issues.

Keep the report concise. Only flag actionable findings. If clean, say so.
```

## Cron Job Setup

```
cronjob create
  name: "Weekly Security Sweep"
  schedule: "0 9 * * 1"      # Every Monday 9am
  model: {provider: "openai-codex", model: "gpt-5.1-codex-max"}
  deliver: "telegram:1505823420"
```

## Why Codex

GPT-5 has broader threat knowledge and better pattern matching than DeepSeek for security analysis. The weekly sweep costs ~one Codex conversation per week — negligible for the value.

## What It Catches

Historical findings that would have been caught:
- Clash root daemon running unsigned binary from user-writable path (CRITICAL)
- macOS firewall disabled with wildcard listeners exposed (HIGH)
- OpenClaw gateway still running after migration to Hermes (MEDIUM)

## Limitations

- Read-only — cannot fix issues, only reports them
- Cannot check browser extensions, TCC permissions, or FileVault from non-admin context
- Relies on gateway being up for delivery (mitigated by watchdog)
