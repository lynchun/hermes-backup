# Typst for Professional PDFs

Typst is a modern typesetting system that replaces LaTeX. It's ideal for reference sheets, reports, and any document where professional typography matters.

## Why Typst over Chrome HTML→PDF

| | Chrome Headless | Typst |
|---|---|---|
| Text selectable | No (rasterized) | Yes (vector) |
| File size | 95MB (48 images) | Similar with images |
| Deterministic | Browser quirks | Always same output |
| Dependency | Chrome.app required | `brew install typst` |
| Typesetting | CSS hacks | Proper engine |

## Installation

```bash
brew install typst  # macOS
```

## Basic Template

```typst
#set page(paper: "a4", margin: (top: 10mm, bottom: 8mm, left: 10mm, right: 10mm))
#set text(font: ("Helvetica Neue", "Hiragino Sans"), size: 10pt, fallback: true)

// Title
#align(center)[
  #text(size: 22pt, weight: "light", tracking: 4pt, fill: rgb("#3a4f1f"))[TITLE]
]

// Content function
#let entry(name, def, img_path) = {
  grid(
    columns: (1fr, 42mm), rows: (auto), gutter: 3mm,
    [
      #text(size: 13pt, weight: "semibold")[#name]
      #text(size: 8pt)[#def]
    ],
    image(img_path, width: 100%, height: 36mm, fit: "cover"),
  )
  v(2mm)
  line(length: 100%, stroke: 0.5pt + rgb("#d4c9a8"))
  v(2mm)
}

// Page number
#align(center)[#text(size: 7pt, fill: rgb("#d4c9a8"))[— 1 —]]
```

## Pitfalls

- **Image paths**: Typst resolves relative to the `.typ` file location. Copy images to the same directory or use relative paths. Absolute `/Users/...` paths may not resolve if `/tmp` is a symlink to `/private/tmp`.
- **Font fallback**: Set `fallback: true` on `#set text()` to avoid errors when CJK fonts are missing. Typst will use available system fonts.
- **`@page` margin boxes**: Like Chrome headless, Typst doesn't use CSS `@page` boxes. Embed page numbers in the body.
- **Do NOT use**: `weasyprint` (missing libgobject on macOS), `cupsfilter` (68-byte broken output), `wkhtmltopdf` (not in Homebrew).
