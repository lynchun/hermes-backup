# Forensic Audit Workflow: Cross-Referencing Management Accounts with Emails

When Lyndon asks you to audit financial records (management accounts, fee
schedules, invoices) against the email record, follow this systematic approach.

## Workflow

### Step 1: Extract All Attachments from Emails

Before any analysis:
- Parse every .eml file in the de-identified folder
- Extract all attachments (PDFs, Excel, Word, images) as standalone files
- Organise by source folder → year-month → email subject
- Verify attachments survived de-identification (check file headers)

Many critical documents live ONLY as attachments — not in email body text.
If you skip this step, you're analysing with blind spots.

### Step 2: Survey What You Have

List everything by type before diving in:

| Type | What to look for | Why |
|------|------------------|-----|
| Excel | Management accounts, fee schedules, cash flows | Actual financial data |
| Word | Quarterly narrative reports | BMM's own descriptions |
| PDF | Signed agreements, loan docs, amendments | Contractual obligations |
| Images | Screenshots, signed doc scans, billing evidence | Often the key evidence |

### Step 3: Build a Comparative Table Across All Periods

Parse each quarter's management accounts systematically. Extract:

- **Income statement** (sheet 3 typically): every expense line with values
- **Balance sheet** (sheet 2): cash, bank balances, assets, capital
- **Cash flow** (sheet 4): large transfers, capital movements, fees paid

Compare values side by side across all quarters. Use a script to do this,
don't read files manually — there are often 20+ quarters.

### Step 4: Look for Specific Red Flags

These patterns emerged from a real audit of Diluca management accounts:

| Red Flag | What to Check | Why It's Suspicious |
|----------|---------------|---------------------|
| **Frozen cash balance** | Is the "Cash" line identical across ALL quarters? | A genuine operating account changes every period. Static = placeholder, not real. |
| **Identical expense values** | Are Accountancy, Legal, Nottary, Service Charge the same number every quarter? | These should be actual monthly expenses. Identical values suggest budget/placeholder figures. |
| **Management fee only recorded once** | Does the Management Fee line appear in every quarter? | A contract requiring quarterly fees should show quarterly entries. |
| **€0 where there shouldn't be** | Are expected revenue/expense lines blank or zero? | Missing entries = unbilled items or poor record-keeping. |
| **Large fund movements** | Are there "Capital transfer" or "Property Sale" entries that don't match known events? | Cross-reference with email discussions about sales, freezes. |
| **Bank balance vs freeze status** | Does the bank balance change during a period when the account was supposedly frozen? | The account can't be frozen if transactions are moving through it. |
| **Duplicate labels** | Are there two lines with similar names (e.g. "Management fee" AND "BMM Management fee")? | Suggests confusion about what's being tracked. |

### Step 5: Cross-Reference with Emails

For each anomaly found in the accounts, search the email corpus for:

- The specific date or period of the anomaly
- Any mention of the transaction, fee, or issue
- Emails where the client asked questions about it
- BMM's responses explaining it
- Any attached documents or screenshots referenced

### Step 6: Quantify the Discrepancies

For findings like "hourly charges outside the PMA":

1. Extract the totals from the evidence (spreadsheet, invoice, email)
2. Verify against what the contract allows
3. Calculate the difference
4. Note which parts the user has already disputed (and when)

### Step 7: Document What the Evidence DOES and DOESN'T Show

Include a mandatory section titled something like:

> ### What the Evidence Does NOT Establish
> - [Fact 1] — no direct email evidence found
> - [Fact 2] — only inferred from dates, not confirmed

This is critical. Lyndon relies on you to distinguish between what's proven
and what's assumed. Overconfident analysis that turns out wrong damages
credibility before client meetings.

## Real-World Example: Diluca Accounts Audit

From a session reviewing 17 quarters of management accounts:

### What Was Found
- Cash frozen at €3,779.32 for 17 consecutive quarters
- Identical expense values across all quarters for 11 categories
- BMM Management Fee recorded only once (Q2 2022: €11,839)
- €511K disappeared from NBG account despite account supposedly being frozen
- "Loan given Omirou" recorded as an expense (should be balance sheet)
- €10 trillion erroneous entry in cash flow statement

### User's preference for output
- **Save findings as .docx** (textutil convert) — Lyndon finds .md hard to read without formatting
- **Include tables** for comparative data — they're faster to scan than paragraphs
- **Bold the critical questions** — formatting helps focus the discussion
