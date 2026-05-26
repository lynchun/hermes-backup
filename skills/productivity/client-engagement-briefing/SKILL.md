---
name: client-engagement-briefing
description: "Produce plain-language briefing papers analyzing a client's commercial relationship with a third-party service provider. Reviews agreements, correspondence, and financial documents to identify breaches, rights, and options. Deliverable: a .docx briefing written as if a professional is explaining the situation to the client in simple terms."
---

# Client Engagement Briefing

Analyze a client's relationship with a third-party service provider, identify issues, and produce a plain-language briefing paper. Designed for AFSL advisers managing client investments where service-provider disputes arise.

## When to Use

- A client has a signed agreement with a service provider (property manager, fund manager, builder, etc.)
- Issues have arisen that may involve breach of contract, negligence, or other misconduct
- You need to produce a plain-language briefing explaining: what happened, what rights were violated, and what options exist
- The client needs to understand their position clearly without legalese

## Core Workflow

### Step 1: Gather and Read Core Documents

| Document | What to extract |
|----------|-----------------|
| **Service Agreement / Contract** | Key obligations, fee structure, liability limitations, dispute resolution clause, governing law |
| **Loan / Financial Agreements** | Who is lender vs borrower? Interest rate, what it applies to, who benefits |
| **Email Correspondence** | Timeline of events, promises made, issues admitted, evidence of notification or lack thereof |
| **Client's Summary / Brief** | The client's perspective on what went wrong — this sets the scope |

**Critical: verify attachments.** When an email references "please see attached agreement" or "as per the enclosed document," find and read that document. Do not rely on the email's summary — the email author may frame it one way while the actual document says something different.

### Step 2: Build the Obligations Map

For each obligation in the agreement, map it to:
- **The contractual clause** (what does the agreement say?)
- **The practical meaning** (what does this mean in plain English?)
- **The evidence** (did they do it? what did the emails show?)
- **The breach assessment** (is there a prima facie breach?)

Use a table format — this becomes the backbone of the briefing paper.

### Step 3: Build a Timeline from Correspondence

Extract key dates from emails and order them chronologically. Include:
- When the agreement was signed
- When each property/assets was acquired/set up
- When each issue first appeared
- When the client was notified (vs when the provider knew)
- Current status

### Step 4: Identify Breaches, Rights, and Defences

For each issue, assess:
- **Right violated** — what obligation was broken?
- **BMM's likely defence** — what will they say in response?
- **Counter-argument** — why that defence is weak
- **Strength of claim** — strong / arguable / weak

### Step 5: Write the Briefing Paper

**Tone and format (Lyndon's preference):**

Write it as if you are a professional briefing your clients in simple terms:
- "Karina and Jim, this briefing explains what happened..."
- Use headings, subheadings, and short paragraphs
- Tables for comparative information
- Bullet points for lists of issues or rights
- **No legalese.** Every legal concept gets a plain-English explanation
- **No hedging.** State the position clearly: "BMM appears to be in breach on three fronts" not "it could be argued that..."
- End with a summary of recommended actions in numbered steps

**Production format:** Generate as a `.docx` file (using python-docx) so the client can open it in Word or Pages. Include:
- Title page with "CONFIDENTIAL" and date
- Five sections matching the brief: obligations, provider actions, timeline, rights/options, legal concepts
- A summary of recommendations at the end

### Step 6: Explain Legal Concepts in Simple Terms

For each legal concept relevant to the case, write a short explainer:

| Concept | Plain English |
|---------|--------------|
| Breach of contract | Breaking a promise written in a signed agreement. Both sides must do what they promised. |
| Gross negligence | More than a simple mistake — a serious failure showing disregard for obligations. |
| Consequential loss | Losses that flow indirectly from a breach (excluded by many contracts, unless gross negligence). |
| Conflict of interest | When someone has a personal interest that conflicts with their duty to the client. |
| Set-off / offset | If A owes B and B owes A, they can net the amounts. Simple, avoids court. |
| Duty to inform | A legal obligation to proactively tell someone about things that affect them. |
| Standard of care | The benchmark for measuring competent performance — what would a competent professional have done? |

## Section Structure for the Briefing Paper

1. **Part 1: What [Provider] Owed the Client — Legally and Ethically**
   - Table of key contractual obligations with plain-English meaning
   - Ethical duties beyond the written contract

2. **Part 2: What [Provider] Actually Did**
   - What they got right (fairness matters)
   - What went wrong (organised by issue, not chronologically)

3. **Part 3: Timeline**
   - Clean chronological table of key events

4. **Part 4: Rights, Breaches, and Options**
   - Rights violated (bullet points)
   - Provider's legal position and likely defences
   - Client's options (from simplest/cheapest to most complex)

5. **Part 5: Legal Concepts in Simple Terms**
   - One paragraph each, no jargon

6. **Summary of Recommendations**
   - Numbered action items the client can take

## Pitfalls

- **Missing the attachment.** When an email references an agreement/attachment and you don't read the actual document, you'll get the legal relationship wrong. Always search for referenced documents in the user's folder tree. Read the agreement, not just the email's summary of it.
- **Misidentifying lender vs borrower.** A "loan amendment" might mean one thing if the client is the lender and another if the client is the borrower. Check the parties listed at the top of the agreement.
- **Over-explaining.** The client knows their own situation. You don't need to restate the background they just gave you — you need to analyse it.
- **Hedging too much.** "It could be argued that BMM may have potentially breached" is weak. "BMM breached clause 5.1(a) by failing to monitor compliance" is clear and useful. The paper is already caveated as "not legal advice" — within that framing, state positions firmly.
- **Wrong deliverable format.** The user wants a `.docx` file they can open directly, not a markdown document or inline text. Use `python-docx`.
- **Including opinions as fact.** Distinguish between: (a) what the agreement says, (b) what the emails show, (c) what your analysis concludes. The first two are evidence; the third is assessment. Label them clearly.

## Scripts

- `scripts/generate_briefing_docx.py` — Python script that produces the `.docx` briefing paper (see reference for structure)
