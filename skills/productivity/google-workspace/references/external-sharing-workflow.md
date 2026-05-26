# External Sharing Workflow — Drive HTML/PDF Viewer

Google Drive requires sign-in to preview HTML files, even with `anyone` link sharing. PDFs render fine in the browser without login, but even PDF previews show a sign-in prompt on the standard `drive.google.com/file/d/.../view` URL.

## The Problem

| File Type | `drive.google.com` preview | Direct download link |
|-----------|---------------------------|---------------------|
| HTML | Requires sign-in | N/A |
| PDF (`webViewLink`) | Shows sign-in prompt | Works (`uc?export=download`) |

## Workaround: Google Docs Viewer (no sign-in needed)

Use the **Google Docs Viewer** URL pattern, which renders any PDF inline without requiring the viewer to be signed in:

```
https://docs.google.com/viewer?url=DIRECT_DOWNLOAD_URL&embedded=true
```

Where `DIRECT_DOWNLOAD_URL` is the `drive.usercontent.google.com` URL:

```
https://drive.usercontent.google.com/download?id=FILE_ID&export=download
```

## Full Workflow

1. **Convert HTML → PDF** locally (Playwright or similar)
2. **Upload PDF** to Drive with `anyone` reader permission
3. **Construct the viewer link** using the uploaded PDF's file ID
4. Share the viewer link — no login required, prints via Cmd+P

## Example

```python
file_id = "1hOEFKxtWaR1fMR76v5gEq4Xf0wqWeWQA"
viewer_url = f"https://docs.google.com/viewer?url=https://drive.usercontent.google.com/download?id={file_id}&export=download&embedded=true"
```

## Pitfalls

- The `export=download` query param is required — without it the URL redirects to a Google login page.
- The `embedded=true` param removes the Drive chrome (file header, sign-in button) — use for cleaner presentation. Without it, the viewer still works but shows Drive UI elements.
- HTML files uploaded to Drive CANNOT be viewed this way — only PDFs work in the Google Docs Viewer.
- Files shared with `anyone` + `reader` role are NOT indexed by Google — they're only accessible via the direct link.
