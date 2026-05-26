---
name: client-matter-analysis
description: Analyse a client's contractual/commercial dispute with a third-party service provider. Read the brief, review agreements and correspondence, then produce a structured analysis covering obligations, timeline, breaches, defences, options, and legal context.
---

# Client Matter Analysis

Analyse a client dispute with a third-party service provider — typically for an AFSL adviser whose client has engaged a property manager, fund manager, or other professional and things went wrong.

## Core Principle: Evidence-Based Analysis (User Correction)

**Do NOT take the client brief at face value.** This was a direct user correction from the BMM matter. The brief tells you the client's *perspective* — your job is to independently verify every claim against source documents (emails, accounts, agreements). 

Approach every analysis as though you're a forensic auditor: cross-reference data, identify red flags, challenge assumptions, and flag gaps where the evidence doesn't support the claim.

The final product should be structured as: "Here is what the evidence shows" — not "Here is what the client told me."

## Workflow

### Step 1: Read the Brief

Start with the user's project brief. It defines the scope of the analysis and tells you:
- Who the parties are
- What the engagement was about
- What went wrong (from the client's perspective)
- What outcome the client is looking for

### Step 2: Read the Key Agreement(s)

Identify and extract the relevant contract. Key clauses to focus on:

| Clause | Why It Matters |
|--------|---------------|
| Scope / Definition of Project | Shows what the provider was actually hired to do |
| Standard of care / skill required | Basis for negligence/breach claims |
| Fee structure | Determines if charges were authorised |
| Compliance/legal obligations | Especially relevant for cross-border or regulated matters |
| Communication/reporting duties | Often breached in client disputes |
| Liability limits, exclusions | Key defence — look for carve-outs (gross negligence, wilful misconduct) |
| Dispute resolution | Mandatory path (mediation, arbitration, jurisdiction) |

### Step 3: Review Correspondence (Emails)

Search the de-identified emails for:
- **Admissions** — the provider acknowledging problems, delays, or failures
- **Explanations** — their account of what went wrong and why
- **Promises** — commitments to fix issues (especially useful if the same problem recurred)
- **Request timelines** — when the client asked for information vs when they got it
- **Unauthorised actions** — charges, payments, or decisions made without client knowledge

### Step 4: Structure the Analysis

Use this template. It mirrors Lyndon's preference for concise, practical, plain-English analysis:

```
## 1. The Engagement — What [Provider] Contractually Owed
[Table: obligation | contractual basis | practical meaning]

## 2. What Actually Happened — Timeline of Issues
[Phase-based narrative: Setup → First problem → Recurrence → Current state]

## 3. Rights Violated & Breaches Established
[For each breach: obligation | what happened | why the provider is vulnerable]
Label strength: Strong case / Clear / Arguable

## 4. [Provider]'s Likely Defences & Responses
[Table: defence | counter-argument]

## 5. Client's Legal Options
[Option A: simplest/lowest cost → Option D: formal proceedings]

## 6. Simple Legal Context
[Table: legal concept | plain English | why it matters for this case]

## 7. Recommended Next Steps
[Actionable items in priority order]
```

### Step 5: Save the Analysis

Write to a markdown file alongside the project brief (or as specified by Lyndon). Use a clear filename like:

```
[Client]_[Provider]_Initial_Analysis.md
```

## Output Principles

- **Concise, structured, plain English.** Avoid legalese. Explain legal concepts simply.
- **Table-heavy format.** Obligations, defences, and options are easiest to digest in table form.
- **Label claim strength** (Strong case / Clear / Arguable) so Lyndon can triage.
- **Include a warning box** for any document the client should NOT sign (e.g. amendments that benefit the other party).
- **End with actionable next steps** in priority order.

## Pitfalls

- **Don't give legal advice.** Frame your analysis as "this is what the position appears to be" and recommend HK counsel for specific questions (especially liability exclusions, gross negligence carve-outs, and jurisdiction-specific issues).
- **Don't over-claim on fiduciary duties.** Fiduciary duties are jurisdiction-specific and fact-dependent. Flag them as "arguable" or "may apply" unless the agreement explicitly creates them.
- **Watch for Multiple Date headers.** Forwarded .eml files often contain Date lines from the forwarded content. Use `email.parser` and `msg.get('Date')` for the actual send date, not raw regex.
- **Recurrence is the killer fact.** A single mistake is an error. The same mistake twice after promises to fix it supports gross negligence arguments.
- **Consequential loss exclusions are central.** Nearly every professional services contract tries to exclude them. The path around them is typically a gross negligence / wilful misconduct carve-out.
- **Check whether fees charged match the contract.** If the contract specifies fixed management/performance fees but the provider also billed hourly staff time, that's an immediate breach for recovery.
- **Forensic audit the management accounts.** If the client provides financial records (spreadsheets, management accounts), compare figures across periods. Watch for: identical expense values across quarters (budgeted, not actual), frozen cash balances that never change, two separate fee lines for the same thing, loans recorded as expenses (misclassification), large unexplained transfers, and spreadsheet errors (like €10 trillion entries). These are red flags that may point to deeper issues.
- **Peer-review your own output before delivery.** After completing the analysis document, verify it yourself — run the numbers, check the dates, cross-check citations. Don't rely on the client to do quality assurance. Direct user instruction: "When you claim it's all done, make sure you check it to see that it IS done, like personal peer review."
- **Flag what the evidence doesn't show.** Include a "Gaps" section explicitly noting claims the client made but you couldn't verify from source documents. This protects both you and the client — they know what's solid and what needs more digging.

## Example

A full worked example is available in `references/bmm-worner-analysis-example.md` — this was a real client dispute where BMM (a Hong Kong property management firm) was engaged to manage Greek property investments for an Australian client, with multiple account freezes, unauthorised billing, and undisclosed personal payments by the principal.
