---
name: macos-security-hardening
description: Scan and harden macOS security posture -- firewall, launch daemons, persistence, SSH, and scheduled Codex-powered audits.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [security, macOS, audit, firewall, hardening]
---

# macOS Security Hardening

Routine security sweep and hardening for macOS. Covers the standard audit checklist and the weekly Codex-powered security cron.

## When to Use

- User asks for a security review or audit
- After installing new software that adds launch daemons
- Setting up recurring security monitoring

## Audit Checklist

Run these read-only checks (never modify without explicit approval):

### 1. Launch Daemons & Agents
```bash
# System daemons (root context)
ls /Library/LaunchDaemons/
# User agents
ls ~/Library/LaunchAgents/
# Check each for user-writable executable paths
# Flag unsigned binaries: codesign -dv /path/to/executable
```

**Red flag:** A system daemon (`/Library/LaunchDaemons/`) whose executable lives in a user-writable path (`~/`). This is a privilege escalation vector.

### 2. Firewall
```bash
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```
Enable if off: `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on`

### 3. System Integrity
```bash
csrutil status          # SIP
spctl --status          # Gatekeeper
fdesetup status         # FileVault
systemsetup -getremotelogin  # SSH
```

### 4. Listening Ports
```bash
lsof -iTCP -sTCP:LISTEN -P -n
```
Flag: non-localhost listeners (`*:PORT` not `127.0.0.1:PORT`)

### 5. SSH
```bash
ls -la ~/.ssh/          # Should be 700
cat ~/.ssh/authorized_keys 2>/dev/null  # Should be empty or known keys only
```

### 6. Persistence
```bash
crontab -l 2>/dev/null
osascript -e 'tell application "System Events" to get the name of every login item' 2>/dev/null
```

## Disabling Privileged Daemons (Without Deleting)

To stop a daemon but preserve files for possible restoration:

```bash
# 1. Unload from launchd
sudo launchctl bootout system/com.example.daemon

# 2. Move plist out of LaunchDaemons (won't auto-start on boot)
sudo mv /Library/LaunchDaemons/com.example.daemon.plist ~/Desktop/daemon.plist.disabled
```

To restore: move plist back and reboot.

## Weekly Security Sweep (Codex Cron)

A weekly cron job using Codex (GPT-5) for threat analysis:

```
cronjob create:
  schedule: 0 9 * * 1       # Mondays 9am
  provider: openai-codex
  model: gpt-5.1-codex-max
  deliver: telegram:CHAT_ID
```

The prompt should cover: launch daemons, firewall, SIP, SSH, listening ports, persistence, kernel extensions, and applications. Codex is preferred over DeepSeek for security reasoning because of broader threat knowledge.

## Removing OpenClaw (post-Hermes migration)

If OpenClaw was replaced by Hermes:
```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
rm ~/Library/LaunchAgents/ai.openclaw.gateway.plist
rm -rf ~/.openclaw
npm uninstall -g openclaw
```

## Common Threats Found

| Finding | Severity | Fix |
|---------|----------|-----|
| Clash daemon from user path | High | Bootout + move plist |
| Firewall disabled | Medium | `socketfilterfw --setglobalstate on` |
| Old agent plists (OpenClaw, etc.) | Low | Remove if superseded |
| Non-localhost listeners | Varies | Review per-service |
