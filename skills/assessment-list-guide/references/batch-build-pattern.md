# Multi-List Batch Build Pattern

Pattern proven on a 5-list, ~295-item assessment guide batch build (May 2026).

## Architecture

Each list gets its own Python data file at `~/Desktop/{name}_data.py`:

```python
ITEMS = [
    (name_en, name_zh_TW, name_ja, image_filename, def_en, def_zh_TW, def_ja),
    ...
]
```

This single source-of-truth feeds both image generation and HTML building.

## File Convention

- `image_filename`: lowercase, underscores, no spaces. e.g. `bighorn_sheep`, `english_horn`
- `name_zh_TW`: Traditional Chinese (Taiwan standard)
- `name_ja`: Japanese
- `def_*`: 1-2 sentences per language

## Build Order

1. Write ALL data files first (write_file, sequential — ~1s each)
2. Start ComfyUI image generation in background (parallel to other work)
3. For Colors lists: generate solid swatches programmatically, no ComfyUI needed
4. Build HTML from data files + image paths
5. PDF conversion
6. Full QC

## Anti-Patterns

- **Subagents for translation data**: claimed completion, wrote nothing. Use `write_file` directly.
- **Bash pipe scripts in cron**: SIGPIPE kills embedded Python. Use standalone `.py` scripts.
- **Mirroring deep folder trees to OneDrive**: path length limits. Use tar.gz archive instead.
