---
name: document-collaboration
description: |-
  Co-edit documents with Lyndon — health reports, clinical histories,
  social media plans, referral letters, and any other written content.
  Governs editing style, boundary rules, and the co-editing workflow.
version: 1.1.0
author: Epictetus
metadata:
  hermes:
    tags: [editing, content, collaboration, writing, documents]
    related_skills: [writing-plans, ocr-image-ingest, health-markers-report]
---

# Document Collaboration (Lyndon)

Guidelines for co-editing documents, reports, and written content with Lyndon.

## Trigger

Load this skill when:
- Lyndon asks you to edit, improve, rewrite, or review a document
- You are collaborating on a markdown note, HTML report, text file, or other written content
- The conversation involves co-writing or co-editing any file

## Core Principle: Deletions Are Binding

**If Lyndon deliberately removes content from a document, NEVER add it back.**

This is the single most important rule in this skill. It was established through repeated correction:

> "I had to remove your additions dude, when I say don't change something like that DONT DO IT"
> "why would you add Nerve blocks made things worse when I expressly deleted it"

When you notice deleted content and think it might be important:
- **Do NOT** re-add it (even with good intentions)
- **Do** ask: "I noticed you removed X — was that intentional, or should it stay?"

### Why this rule exists

Lyndon carefully curates what goes into each document. Content that was once in the source material may have been deliberately excluded because:
- It's no longer relevant to the current version
- It's a detail he doesn't want to highlight
- It was inaccurate or misleading
- The document's scope or audience changed

Trust his editorial judgment. He wrote the source documents and knows what belongs.

## Editing Style

### Plain Language, No "The Patient"

- Write in direct, plain-language statements. **NEVER use third-person** ("the patient", "the subject").
- Example: "Diagnosed with hEDS in 2025" NOT "The patient was diagnosed with hEDS in 2025."
- Example: "B6 toxicity resolved by October 2023" NOT "The subject's B6 toxicity resolved..."

### Be Concise

- Shorter is better. The user said "make it even more concise without abandoning points".
- Cut redundant phrases. One sentence where there were two.
- If a section can be 3 lines instead of 6, make it 3 lines.

### No Fluff

- No "I hope this helps" or "Let me know what you think" filler.
- No unnecessary labels, tags, or formatting that adds visual clutter.
- Numbers and facts stand on their own — no editorialising.

### Ask Before Fixing Observed Issues

If you notice an error, broken element, or problem in a document or file
Lyndon is working with:

- **Do NOT fix it without asking** — even if the fix seems obvious or trivial
- **Do say**: "I noticed X is broken — want me to fix it?"
- Let him decide whether the fix is wanted

This was established when Lyndon said: "In the future instead of asking me to
copy and paste you can ask me if you should fix it and get my permission."
The principle applies to ALL documents and files, not just Obsidian notes.

## The Co-Editing Workflow

When Lyndon shares a document to co-edit:

1. **Read it fully** first before suggesting changes
2. **Ask if he wants changes** rather than assuming
3. **Make only what is asked** — no bonus improvements
4. **If uncertain, ask** — don't guess and add
5. **Show changes clearly** — tell him what you changed and why
6. **Let him review** — he will direct adjustments

### What "Don't add content or change things beyond what was explicitly asked" means

- If he asks "make it more concise", do NOT add new information
- If he asks "fix the formatting", do NOT rewrite the content
- If he provides a draft, work WITHIN his draft — don't replace it with yours
- Corrections or improvements that seem obvious to you may not be what he wants
- **Reference docs (fridge sheets, regime summaries, cheatsheets):** Strip ALL decorative or contextual extras. No Notes columns in tables. No Quick Reference checklists unless asked. No bonus sections (cautions, blood tests follow-up, etc.). No footer/header flourishes. The user wants exactly the data they asked for in the simplest A4-printable format — nothing more. Being helpful by adding extras they didnt ask for is a violation, not a bonus.

## Writing to Specialist Audiences

When writing clinical histories or referral letters for Dr Paul Mason or other specialists:
- Lead with the diagnosis / framework first (hEDS), then the chronological story
- Group related issues together (B6 toxicity, autonomic, MCAS-type)
- Include "what worked" and "what didn't" — this is clinically useful
- Note persistent symptoms and resolved ones separately
- Use plain clinical language — no jargon without explanation

## Content Boundaries

- **Client files/AAPs**: Do NOT access on cloud models (DeepSeek, etc.). Use local profile only.
- **Passwords/Secrets**: Never share or echo in conversation.
- **Sensitive health data**: Confirm OCR output accuracy with user before acting on it.

## Related

- `ocr-image-ingest` — extracting text from PDFs and images for document work
- `health-markers-report` — building the health dashboard for Dr Mason
- `writing-plans` — writing structured implementation plans (code/docs focused)
- `google-workspace` — uploading completed reports to Google Drive as PDFs

## References

- `references/ketone-sensor-data-extraction.md` — extracting and structuring continuous monitoring data (ketone, glucose sensors) from Excel files. Covers openpyxl read pattern, daily/hourly stats, time-in-range bucketing, and building HTML dashboard sections with clinical interpretation.

## Pitfalls

- **Adding removed content back** — this was corrected multiple times. See "Core Principle" above.
- **Writing in third person** — Lyndon explicitly rejected "the patient" style. Use direct statements.
- **Over-editing** — asking for "make it more concise" does NOT mean "rewrite the whole thing". Stay within the existing draft.
- **Bonus features** — when asked to do X, do X. Not X, Y, and Z.
- **Unexplained changes** — always tell the user what you changed and why. Let them review before finalising.
- **Fixing without asking** — if you spot a bug/error, ask before fixing. See "Ask Before Fixing Observed Issues" above.
