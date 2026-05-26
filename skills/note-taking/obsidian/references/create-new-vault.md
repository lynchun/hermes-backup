# Creating a New Obsidian Vault

The `obsidian` skill assumes an existing vault. Use this reference when you need to create a brand-new vault from scratch.

## Vault location

Obsidian vaults on macOS live in:
- iCloud: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<VaultName>`
- Local: `~/Documents/<VaultName>`

The iCloud location syncs across devices. Prefer it unless the user specifies otherwise.

## Minimum vault structure

```
<VaultName>/
  .obsidian/
    appearance.json
    community-plugins.json
    core-plugins.json
```

### appearance.json

Controls theme and accent colour. Minimal viable:

```json
{
  "baseTheme": "moonstone",
  "accentColor": "#1e1e2e"
}
```

### community-plugins.json

List of community plugin IDs to enable. Useful plugins for diagramming:

```json
["obsidian-excalidraw-plugin", "obsidian-mermaid"]
```

Mermaid renders natively in Obsidian with no plugin needed — but `obsidian-mermaid` can be listed for completeness. Excalidraw requires the community plugin.

### core-plugins.json

Controls built-in features. Minimal viable for a structured vault:

```json
{
  "file-explorer": true,
  "global-search": true,
  "graph": true,
  "backlink": true,
  "canvas": true,
  "tag-pane": true,
  "page-preview": true,
  "templates": true,
  "command-palette": true,
  "editor-status": true,
  "bookmarks": true,
  "word-count": true,
  "file-recovery": true,
  "properties": true
}
```

## Creating Excalidraw diagrams

Excalidraw files use `.excalidraw` extension and are valid JSON. A minimal diagram:

```json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {
      "id": "box1",
      "type": "rectangle",
      "x": 50,
      "y": 100,
      "width": 180,
      "height": 80,
      "strokeColor": "#2b8a3e",
      "backgroundColor": "#d3f9d8",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roundness": {"type": 3},
      "boundElements": []
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

The first time the user opens the vault, Obsidian will prompt to trust the author and enable community plugins.

## Linking from notes

Add a reference at the bottom of the main index note so users can find the Excalidraw version:

```
See [[Excalidraw/Diagram Name]] for the visual version.
```

## Folders for structured vaults

Good default folders for a process/OS-style vault:

```
Operating System/    — workflows, processes, flowcharts
Templates/           — reusable prompt templates, checklists
Assets and Guidelines/ — style guides, safety rules, governance
Excalidraw/          — visual diagram files
```
