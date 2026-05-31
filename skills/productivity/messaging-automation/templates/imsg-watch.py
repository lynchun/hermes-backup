#!/usr/bin/env python3
"""Poll iMessage for new incoming messages since last check.
Drop-in template — adapt IMSC path and platform logic for other messengers.

Usage: set up as a no_agent cron job with deliver='local'.
The agent checks the inbox file during active sessions.
"""
import json, os, subprocess, sys
from datetime import datetime, timezone

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
STATE_FILE = os.path.join(HERMES_HOME, ".imsg_last_check")
INBOX_FILE = os.path.join(HERMES_HOME, ".imsg_inbox")
IMSC = "/opt/homebrew/bin/imsg"

def main():
    # Read last checkpoint
    last_check_str = ""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            last_check_str = f.read().strip()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(STATE_FILE, "w") as f:
        f.write(now)

    if not last_check_str:
        return  # first run, just seed

    last_check = datetime.fromisoformat(last_check_str.replace("Z", "+00:00"))

    # === PLATFORM-SPECIFIC: get recent conversations ===
    result = subprocess.run(
        [IMSC, "chats", "--limit", "20", "--json"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        sys.stderr.write(f"imsg chats failed: {result.stderr[:200]}\n")
        return

    found = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            chat = json.loads(line)
        except json.JSONDecodeError:
            continue

        # === PLATFORM-SPECIFIC: parse last message timestamp ===
        last_msg_ts = chat.get("last_message_at", "")
        if not last_msg_ts:
            continue
        msg_time = datetime.fromisoformat(last_msg_ts.replace("Z", "+00:00"))
        if msg_time <= last_check:
            break  # chats sorted by recency — nothing newer beyond this

        chat_id = chat["id"]
        contact = chat.get("contact_name", "") or chat.get("chat_identifier", "unknown")

        # === PLATFORM-SPECIFIC: get recent messages for this chat ===
        hist = subprocess.run(
            [IMSC, "history", "--chat-id", str(chat_id), "--limit", "5", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if hist.returncode != 0:
            continue

        for msg_line in hist.stdout.strip().split("\n"):
            if not msg_line.strip():
                continue
            try:
                msg = json.loads(msg_line)
            except json.JSONDecodeError:
                continue
            msg_time = datetime.fromisoformat(msg["created_at"].replace("Z", "+00:00"))
            if msg_time <= last_check:
                continue
            # === PLATFORM-SPECIFIC: filter out own messages ===
            if msg.get("is_from_me"):
                continue
            text = msg.get("text", "").strip()
            if not text:
                continue
            found.append({
                "contact": contact,
                "chat_id": chat_id,
                "identifier": chat.get("chat_identifier", ""),
                "text": text,
                "time": msg.get("created_at", "")
            })

    if found:
        with open(INBOX_FILE, "w") as f:
            json.dump(found, f, indent=2)
        print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {len(found)} new message(s) -> {INBOX_FILE}")
    else:
        print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] no new messages (last_check={last_check_str})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
