---
name: imessage-auto-reply
description: Monitor iMessages via cron polling and draft AI-assisted replies in Lyndon's voice. Covers imsg watcher setup, voice profile, and the draft→approve→send workflow.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, auto-reply, messaging, macOS, voice]
    related_skills: [imessage]
---

# iMessage Auto-Reply

Monitor incoming iMessages and draft responses in Lyndon's voice. Uses a no-agent cron poller with the `imsg` CLI -- zero token cost when no messages arrive.

## When to Use

- Lyndon asks to be notified of iMessage replies
- Lyndon wants AI-drafted responses to review before sending
- Setting up continuous iMessage monitoring

## Prerequisites

- `imsg` installed: `brew install steipete/tap/imsg`
- **Full Disk Access** granted to Terminal (System Settings → Privacy → Full Disk Access)
- **Automation** permission for Terminal to control Messages.app (prompted on first send)

## Voice Profile: Lyndon

When drafting replies, match this style:

| Trait | Pattern |
|-------|---------|
| **Tone** | Casual Australian -- "mate", "dude", "bro", "outta", "locked" |
| **Emoji** | Uses emoji naturally -- 😅 🧐 😂 ❤️ 😊 |
| **Formality** | Warm but efficient. Names people. Gets to the point. |
| **Mum (Ma)** | Brief, practical, uses "u" instead of "you" |
| **Friends** | Banter and jokes, "bro", "dude" |
| **Acquaintances** | Thoughtful full sentences, polite, helpful |
| **Length** | Short with close contacts, longer only when giving advice |
| **Humor** | Self-deprecating where natural |

**Never sound like an AI.** No "Certainly!", "I'd be happy to", "Of course!", or overly polished language. Lyndon's messages are human-first: contractions, occasional typos, no corporate phrasing.

## Workflow

### 1. Setup the watcher cron

The script lives at `~/.hermes/scripts/imsg-watch.sh`. It polls `imsg chats` + `imsg history` every 2 minutes and writes new messages to `~/.hermes/.imsg_inbox`. Cron delivery must be `local`:

```
cronjob create:
  schedule: every 2m
  script: imsg-watch.sh
  no_agent: true
  deliver: local        ← CRITICAL: not 'origin'
```

### 2. Check for messages

When Lyndon is in an active session, check the inbox file:

```bash
cat ~/.hermes/.imsg_inbox
```

Also run the script directly to force a fresh poll.

### 3. Draft response

For each new message:
- Read the contact name and relationship context
- Draft a reply matching the voice profile above
- Present to Lyndon with the original message for approval

### 4. Send after approval

```bash
imsg send --to "+61XXXXXXXXX" --text "approved message"
```

## Pitfalls

### Cron `deliver=origin` does NOT work for CLI

The delivery target `origin` only resolves in gateway platform contexts (Telegram, Discord, etc.) where there's a persistent chat session. In cron, it produces "no delivery target resolved" warnings. For CLI users, use `deliver=local` and have the agent check the output file manually.

See `references/cron-delivery-cli-pitfall.md` for full details.

### State file seeding

On first run, the watcher script seeds the timestamp file and exits. This prevents old messages from flooding in. If you need to catch existing messages, set the timestamp back:

```bash
echo "2026-05-28T00:00:00Z" > ~/.hermes/.imsg_last_check
```

### Microsoft authenticator triggers

Accessing the Messages database via `imsg` may trigger Microsoft authenticator prompts for the iMessage account (`lynchun@hotmail.com`). This is cosmetic -- `imsg` reads the local chat.db directly and doesn't need re-authentication. Deny the prompt.

### No persistent CLI delivery channel

Unlike Telegram where cron can deliver directly to a chat, CLI sessions don't have a persistent delivery target. The inbox file pattern is the workaround. The agent should proactively check it during active sessions.

## Script Reference

The watcher script is at `~/.hermes/scripts/imsg-watch.sh`. Key design:

- Tracks last poll time in `~/.hermes/.imsg_last_check`
- Writes new messages to `~/.hermes/.imsg_inbox` as JSON array
- Only checks chats with `last_message_at` newer than the checkpoint
- Filters out `is_from_me` messages (own sends)
- Uses `imsg chats` (sorted by recency) + breaks early for efficiency
