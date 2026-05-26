---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

> **Reference**: `references/create-new-vault.md` covers creating a new vault from scratch (`.obsidian` config, Excalidraw files, folder structure). Only needed when there is no existing vault to work with.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

### ASK before applying edits

Critical user preference: **Always present the proposed fix first and ask for permission before applying it to any Obsidian note.** The user will review the change, approve it, and only then should the edit be made. Do NOT fix-and-save — always fix-and-show, then save on approval.

This applies to ALL types of edits: Mermaid diagram fixes, content corrections, formatting changes, new notes, appending content — anything that modifies the vault. The user has explicitly corrected this: "fix now, ask first next time."

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Data Verification in Structured Notes

When Obsidian notes contain structured data compiled from external sources (lab results, financials, research extracts), always cross-verify against source documents before trusting or correcting values.

**Workflow:**

1. Identify source files: PDFs, RTFs, DOCXs, CSVs that the Obsidian data was compiled from
2. Extract source text: use `ocr-and-documents` skill (pdftotext for PDFs, textutil for RTF/DOCX)
3. Compare specific date+value pairs between Obsidian notes and source documents
4. Fix discrepancies directly in the .md files using `patch` or `write_file`

**Common issues in compiled health/financial data:**

- **Unit errors**: values that make no sense at stated unit (e.g. 15.4 mmol/L testosterone → nmol/L)
- **Mixed tests**: different analytes lumped under one marker name (e.g. serum iron and TIBC under "Iron")
- **OCR noise**: implausible outlier values from PDF scraping (e.g. Globulin = 8 g/L)
- **Missing entries**: source has data the note doesn't (e.g. historical homocysteine values)
- **Missing markers entirely**: results exist in source with no corresponding .md file
- **g/L vs mg/L swap**: easily confused — CRP at 30.4 g/L is impossible (should be mg/L)

**Pitfalls:**
- Image-based PDFs return blank from pdftotext — try tesseract or marker-pdf instead
- Compound RTFs concatenate multiple reports — check the full file length, not just the first page
- Date fields in lab tables may default to patient DOB instead of collection date
- Multiple values on same date is normal (different labs, different metrics) — don't deduplicate
- **Trust user domain knowledge over compiled CSVs**: when the user says "I know the source document says X, not Y", cite-compare against the actual source. The user's recollection combined with their original documents is more reliable than an automated extraction pipeline that may have misread table columns or mixed historical data rows.
