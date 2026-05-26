# Soulseek Setup for Music Search/Download

Soulseek is a peer-to-peer music sharing network. It's often the only source for high-bitrate versions of old remixes, bootlegs, and free releases that no longer exist on YouTube/streaming.

## Access Methods

### Method 1: Nicotine+ (Brew, headless)

```bash
brew install nicotine-plus

# Create config
mkdir -p ~/.config/nicotine
cat > ~/.config/nicotine/config << 'CFG'
[server]
server = server.slsknet.org
port = 2416
user = YOUR_USERNAME
pass = YOUR_PASSWORD
auto_connect_startup = True
auto_connect_now = True
CFG

# Run headless
/opt/homebrew/bin/nicotine --headless
```

### Method 2: slskd (Docker)

```bash
docker pull slskd/slskd:latest

docker run -d \
  --name slskd \
  -p 15000:5000 \
  -p 15001:5001 \
  -e SLSKD_CREDENTIALS_USERNAME="username" \
  -e SLSKD_CREDENTIALS_PASSWORD="password" \
  -e SLSKD_REMOTE_CONFIGURATION=true \
  -v ~/.slskd:/app/config \
  slskd/slskd:latest
```

Port 5000 = Soulseek client, 5001 = Web UI/API.

### Method 3: aioslsk (Python library)

```bash
pip install aioslsk
```

See `/tmp/slsk_direct.py` from the 2026-05-18 session for a working search script.

## Critical Requirement: You Must Share Files

The Soulseek network heavily penalises users with zero shared files. Other peers may ignore your search requests entirely. **A new account with no shared files will get zero results even when tracks exist on the network.** Before searching, either:
- Configure a directory of music to share (at least a few hundred MB of genuine music, not dummy files)
- Or use an existing account that already has shared files and network reputation

**This is the most common failure mode.** If a search returns empty results, it's almost certainly because the account has no shared files. The Python libraries (aioslsk) and headless tools (slskd, Nicotine+ headless) all fail the same way — they connect fine but other peers ignore their requests.

## Registration

You cannot register a Soulseek account programmatically — the server only creates accounts on first successful login from the official client. Download the official Soulseek client (or Nicotine+ GUI), create your account there (no email needed, just pick a username/password), share at least some music, then use those credentials with Docker/Python tools for headless search.

## Pitfalls

- Generic/new accounts with no shared files get zero search results. This is the most common reason searches return empty.
- Python 3.9 has limited compatibility with newer soulseek Python libraries — prefer brew-installed Python 3.14 or Docker.
- The Soulseek protocol and server have not changed in decades, but client implementations (aioslsk, slskd, Nicotine+) have varying levels of modern network support (SABR streaming, obfuscated connections).
