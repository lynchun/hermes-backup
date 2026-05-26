# Security Audit Checklist

Quick security sweep for a macOS machine running AI agents. Run these commands to
audit what's installed, running, exposed, and what permissions agents have.

## 1. Installed AI Tools
```bash
which hermes claude codex opencode ollama gh 2>/dev/null
hermes --version; codex --version; ollama --version
npm list -g --depth=0 | grep -iE 'claude|codex|copilot|ai|agent'
pip3 list | grep -iE 'openai|anthropic|langchain|llama'
brew list | grep -iE 'hermes|claude|codex|ollama|llama|whisper'
```

## 2. Running Processes
```bash
ps aux | grep -iE 'hermes|claude|codex|ollama|peekaboo|openclaw|gateway|mcp' | grep -v grep
```

## 3. Network Exposure
```bash
# Listening ports
lsof -iTCP -sTCP:LISTEN -P -n | awk '{print $1, $9}' | sort -u
# External connections
lsof -iTCP -sTCP:ESTABLISHED -P -n | awk '{print $1, $9}' | grep -v '127.0.0.1\|localhost' | sort -u
# Firewall
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

## 4. Credentials
```bash
# API keys (redacted)
grep -E '^[A-Z_]+=' ~/.hermes/.env | cut -d= -f1 | sort
# OAuth tokens
hermes auth list
# Keychain count
security dump-keychain | grep -c '0x'
# SSH keys
ls -la ~/.ssh/
# Credential files
find ~/Library ~/.config ~/.hermes -maxdepth 3 -name "*.json" -path "*auth*" -o -path "*cred*"
```

## 5. Permissions
```bash
# Launch agents (boot-time)
ls ~/Library/LaunchAgents/
# Hermes approvals mode
grep -A3 'approvals' ~/.hermes/config.yaml
# Code signing
codesign -dv /opt/homebrew/bin/peekaboo 2>&1 | head -2
codesign -dv ~/.local/bin/hermes 2>&1 | head -2
codesign -dv /opt/homebrew/bin/codex 2>&1 | head -2
```

## 6. MCP Servers
```bash
# Claude MCP config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
```

## 7. Skills & Plugins
```bash
find ~/.hermes/skills -name "SKILL.md" | wc -l
find ~/.hermes/skills -name "*.py" -o -name "*.sh"
hermes curator status
```

## Common Findings

| Issue | Fix |
|-------|-----|
| YOLO mode (approvals off) | `hermes config set approvals.mode smart` |
| Hermes outdated | `hermes update` |
| Dual gateways (Hermes + OpenClaw) | Remove unused: `launchctl remove <label>` |
| Claude MCP filesystem to sensitive dirs | Trim vault list in `claude_desktop_config.json` |
| API keys in plaintext .env | Expected — chmod 600 is sufficient. Move to keychain if paranoid. |
| Unsigned binaries | Expected for CLI tools — no notarization for CLI tools generally. |
| Peekaboo full screen access | Required for desktop automation. Cannot work without it. |
