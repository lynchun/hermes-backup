---
name: lyndon-voice
description: "Lyndon's communication style for drafting iMessages and messages. Load before drafting any outgoing message on Lyndon's behalf."
version: 1.0.0
---

# Lyndon's Voice

Use when drafting iMessages, emails, or any outgoing messages on Lyndon's behalf.

## Core Rules

- **Australian, not ocker.** Casual but not sloppy. No excessive slang.
- **No "mate" in professional contexts.** Friends only.
- **No "yeah" / "nah" in work messages.** Keep work professional.
- **Doesn't say "locked"** (used once, not habitual).
- **No "locked"** (used once historically, not habitual — don't use it)
- **Keto/carnivore. No references to alcohol of any kind** — no wine, no beer, no spirits. Wants meat. Can be flexible but knows what he prefers.
- **Not "easy with food."** Has preferences — don't make him sound indifferent about meals. He wants what he wants (meat) but can flex.

## By Relationship

### Mum (Ma) — +61419606141
- Casual warmth but direct. Knows what he wants.
- Uses "u" occasionally but not every sentence.
- Brief replies OK: "Ok", "Awesome, what time?"
- Food: "I'll just have meat if that works, can be flexible tho"
- Confirms plans simply. Doesn't over-explain.

### Close Friends
- "dude", "bro" are fine. Light banter.
- Self-deprecating humor OK.
- Emoji: 😊 🧐 but don't overuse.

### Work / Professional
- Professional, clear, concise. Measured and analytical.
- Opener: "Hi [Name]," or "Hi Guys," -- never "Hey", never "Dear"
- No "mate", "yeah", "bro", "dude", exclamation marks.
- Full sentences but not stiff. No fluff.
- Polite but direct questions: "Can you please..."
- "We" for Stewards Capital, "I" for personal view.
- Precise with numbers/dates: "EUR at 1.634"
- Uses "re" for regarding, "FYI" sparingly.
- Sign-off: "Regards," then full signature block.
- Strategic/factual tone -- lays out options, doesn't emote.
- Example: "Our options for FX conversion are either done by you before remittance or done by us upon receipt. We are interested in getting the best rate."

### Acquaintances (Jo, Katrina, etc.)
- Warm but not overly familiar.
- Names them in first message: "Hi Jo, ..."
- Helpful, thoughtful. Not curt.

## Process

1. Load this skill when drafting any outgoing message.
2. Draft in Lyndon's voice per the rules above.
3. Present draft for approval.
4. If corrected: update this skill immediately (patch).

## Training Loop

This skill improves through correction. The workflow is:

```
Draft → Lyndon reviews → "that's off because [reason]" → Patch skill → Draft improves
```

Every correction is a gift. When Lyndon flags something wrong:
- **Identify the pattern** — is it a word choice, tone mismatch, factual error?
- **Patch the relevant section** of this skill immediately
- **Add a pitfall** if the mistake would be easy to repeat

Examples of past corrections that improved this skill:
- "locked" — used once in chat history, not habitual → added to Core Rules
- "wine" — Lyndon is keto/carnivore, doesn't drink wine → Core Rules updated
- "I'm easy with food" — sounded indifferent, Lyndon has preferences → Core Rules updated
- Work messages — "yeah mate" was too casual for professional context → Prof. section tightened
- **Professional ≠ conversational.** Lyndon's work emails are clean, direct, and factual. When in doubt, err toward professional rather than casual. The BMM email reference shows the target tone.

## Pitfalls

- **Don't overfit to one message.** A single use of a word ("locked") doesn't make it part of the voice. Err on the side of omitting unusual patterns.
- **Keto/carnivore is a hard constraint.** Never suggest carbs, alcohol, or non-keto foods/drinks.
- **Professional ≠ stiff.** Lyndon's work emails are clear and direct, not bureaucratic.

## Reference Files

- `references/bmm-email-patterns.md` — Real email excerpts from BMM case showing professional patterns
- `references/ma-auto-reply.md` — Ma (mum) conversation rules and cafe timing auto-reply logic
- `references/imsg-watcher.md` — iMessage polling system architecture and debugging guide
