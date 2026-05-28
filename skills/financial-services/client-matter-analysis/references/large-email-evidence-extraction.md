# Large Email Evidence Extraction

When evidence comes from large de-identified email sets (1000+ .eml files spanning years), follow this extraction methodology. This supplements the main workflow's Step 3 (Review Correspondence).

## Handling 1000+ Emails

Don't read every one. Instead:

1. **Map conversations by subject** — threads cluster around topics (fund management, accounts, loan terms, etc.)
2. **Read final/current emails first** — they often summarise the history
3. **Build the timeline as you go** — note key events with dates and sources
4. **Identify repeated patterns** — one-off issues vs systemic failures

### Key Facts to Extract

- Dates of significant events (sale, payment, freeze, notification)
- What the counterparty said they would do
- What they actually did (or failed to do)
- When the client was informed (vs when the client discovered)
- Any admissions or statements against interest

### Attachment Verification

**Critical: verify attachments.** When an email references "please see attached agreement" or "as per the enclosed document," find and read that document. Do not rely on the email's summary — the email author may frame it one way while the actual document says something different.

For forwarded .eml files, use `email.parser` and `msg.get('Date')` for the actual send date, not raw regex — forwarded emails often contain multiple Date lines.

### Output: Evidence Map

After extraction, produce a section structured as:

```
## What the Evidence Shows
- Claim → Supporting source → Strength (Strong / Clear / Arguable)

## What the Evidence Does NOT Establish
- Bullet list of gaps — claims made but not verified from source documents
```

The "What the Evidence Does NOT Establish" section is mandatory — it protects both you and the client by making clear what's solid and what needs more digging.

## Supporting Document Inventory

Before reading emails, inventory the supporting materials:

- Agreements (PMA, loan agreements, addendums) — read the key clauses
- Analysis documents (if any exist) — these may already have legal analysis
- Financial documents (loan schedules, invoices, bank statements)
- Any correspondence summaries or chronologies
