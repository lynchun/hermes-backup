---
name: qc-review
description: "Spawn a subagent QC reviewer to check deliverables against original specifications before delivery. Catch gaps, double-numbering, missing elements, spec violations."
version: 1.0.0
author: Epictetus + Lyndon Arthurson
---

# QC Review Agent

Before delivering any output (PDF, document, code, image set), spawn a subagent as a dedicated QC reviewer. This is NOT the same as self-QC — it's a separate agent with ONLY the spec and the deliverable, no implementation context to bias it.

## Known issues

**delegate_task subagents may crash with `'NoneType' object is not iterable`.** This has been observed repeatedly with Codex subagents doing both QC review and translation work. The error is internal to the delegation system — subagents fail before producing any output.

**Fallback when subagent crashes:** If the QC subagent fails, use direct `vision_analyze` on the deliverable. Convert PDF pages to PNG first:
```bash
pdftocairo -png -f 1 -l 1 -singlefile -scale-to 1200 input.pdf output_p1
```
`sips` cannot select specific PDF pages — always use `pdftocairo` (from poppler: `brew install poppler`). Then run the original spec checklist manually via vision questions on each page.

**Verify blank-page corruption before QC:** Before running vision QC, verify each page has actual content — a corrupted Typst file compiles with exit 0 but produces blank pages. Check file sizes: `pdftocairo -png` output >50KB for content pages (blank pages are <10KB). If a page is blank, the source file is corrupted — regenerate it.

**Do NOT retry crashed subagents more than once.** A second crash confirms the systemic issue — switch to fallback immediately.

## When to use
- Before telling the user something is "done"
- After any multi-step creation workflow (PDFs, reference sheets, galleries)
- When the user has given specific formatting/design requirements

## How to use
**Primary: delegate_task** — spawn a subagent as QC reviewer. This is a separate agent with ONLY the spec and the deliverable, no implementation context to bias it.
- goal: "QC review of [deliverable] against original specification"
- context: Include the EXACT original spec from the user AND any updates they gave
- toolsets: ["vision","file","terminal"]

The QC agent's ONLY job is to flag gaps — not suggest improvements beyond the spec.

## Example prompt
```
ORIGINAL SPEC: [paste user's exact requirements]
USER UPDATES: [any changes they made during iteration]
DELIVERABLE: [file path]
Check: [specific checklist items]
Overall verdict: PASS or FAIL
```

## Rules
1. Always QC before delivering
2. If QC fails, fix and re-QC before showing user
3. The QC agent gets no credit for being nice — it's there to find problems
4. Run QC on every iteration, not just the final version
5. **Give the QC agent the EXACT original spec verbatim** — do NOT paraphrase or summarize. The user's exact words contain requirements that your summary might drop. Copy-paste the original requirement text into the context field.
6. **When the spec evolves during iteration** (user says "also do X" or "change Y to Z"), include ALL updates in the QC context alongside the original spec. The QC agent needs the full picture, not just the latest tweak.
7. **QC agent must check for double-numbering.** Typst `+ enum` lists auto-number and clash with manual numbers. Always verify no "1. 1. Kenya" patterns.
8. **RE-VERIFY AFTER EVERY FIX.** The most dangerous failure mode: you fix a bug, recompile (exit 0), and tell the user it's done — but the fix introduced a new issue or the underlying file was corrupted and you didn't visually check. Typst compiles corrupt source files with exit code 0 producing blank pages. A full page of country index entries silently overflows off the bottom with no error. Always convert the fixed page to PNG and vision-check it before telling the user "done." Never trust a compile exit code alone.
9. **For geographic maps: check Mercator squashing.** High-latitude continents (Europe 33-72°N, North America 5-85°N) get horizontally stretched ~1.6× when plotted in WGS84 without projection compensation. Countries look wide and flat. Fix: `ax.set_aspect(1.0 / np.cos(np.radians(mid_lat)))`. During QC, look at the map and ask: "Do countries look proportionally natural?" If Italy looks fat or Scandinavia looks squashed, it failed.

10. **Check continent shape coherence.** Unshaded countries must be visibly distinct from the page background. If they blend in, the continent looks like disconnected floating green blobs rather than a unified landmass. During QC ask: "Is the continent shape clearly visible as a coherent landmass? Are borders between unshaded countries visible?" Fix: unshaded land `#e8e0d0`, background `#fdfaf3`, borders `#b8af9a` at linewidth 0.4.

11. **Count every index entry.** The bold country index on page 1 must show ALL entries. Entries silently overflow off the bottom — Typst gives no warning. During QC: count the visible index entries and verify the count matches the continent's total. If entries are missing, reduce font size or tighten leading.

12. **Do NOT abandon a project mid-stream when the user mentions something else.** A user saying "let's also do X" or "I want to talk about Y" does NOT mean "stop the current work." Finish the current deliverable before pivoting. If uncertain, ask: "I'm in the middle of [project] — should I pause and switch, or finish this first?" Dropping projects forces the user to re-initiate and creates frustration.

13. **When image generation fails, pivot to deterministic alternatives immediately.** ComfyUI may return HTTP 500 on macOS/Python 3.14/MPS. Do NOT debug — fall back to PIL programmatic illustrations. The user explicitly prefers deterministic, fast results over waiting for broken infrastructure. "If you can do it with less spend on tokens I would much prefer that."

14. **Never use `write_file` in `execute_code` with content from `read_file`.** `read_file` returns content WITH line number prefixes ("1|content"). Passing that to `write_file` corrupts the file with double line numbers ("1|1|content"). Typst compiles corrupted files with exit code 0, producing blank pages. Use `patch` tool for edits, or `write_file` only with freshly-generated content. After any programmatic file write, verify the first few lines are not double-numbered.
