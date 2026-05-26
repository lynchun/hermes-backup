---
name: youtube-download
description: "Download YouTube audio/video at best available quality, handle 403 errors and PO Token issues, extract audio to MP3/FLAC."
version: 1.0.0
author: Epictetus
platforms: [linux, macos]
---

# YouTube Download

Download YouTube audio/video at the best available quality. Handles the common pitfalls around YouTube's 403 Forbidden responses, missing PO Tokens, and audio extraction.

## Setup

```bash
pip install yt-dlp
```

If on Python 3.9, yt-dlp may print deprecation warnings but still works.

## Check Available Formats

```bash
python3 -m yt_dlp -F "https://www.youtube.com/watch?v=VIDEO_ID"
```

Shows all formats with resolution, bitrate, codec, and filesize. Look for:
- `ID` — the format number to pass to download
- High-resolution video (`137`, `299` for 1080p+) 
- Audio-only (`251` = opus 160k, `140` = m4a 128k)
- Combined (`18` = 360p+h264+aac, `22` = 720p)

## Download Audio (Best Quality)

```bash
# Audio-only, auto-convert to MP3 (best quality up to 320kbps where available)
python3 -m yt_dlp -x --audio-format mp3 --audio-quality 0 \
  -o "~/Downloads/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Keep original audio format (opus/m4a) without re-encoding
python3 -m yt_dlp -f "bestaudio[ext=m4a]" \
  -o "~/Downloads/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Download Video (Best Quality)

```bash
python3 -m yt_dlp -f "bestvideo+bestaudio" \
  -o "~/Downloads/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Handling 403 Forbidden Errors

YouTube has been restricting downloads via the default `web` client. When you get `HTTP Error 403: Forbidden`, try the `android` client:

```bash
python3 -m yt_dlp --extractor-args "youtube:player_client=android" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

The android client may produce a warning about missing GVS PO Tokens for higher-quality formats, but the fallback format (typically format 18 — 360p/h264/aac) will still download successfully.

**Proven working command (this session, 2026-05-18):**
```bash
python3 -m yt_dlp --extractor-args "youtube:player_client=android" \
  -x --audio-format mp3 --audio-quality 0 \
  -o "~/Downloads/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```
The `--audio-quality 0` flag requests the best VBR encoding from ffmpeg during the conversion step. The re-encoded quality is capped by the source audio quality.

If even the android client gets 403, the video was likely uploaded with SABR streaming (newer YouTube restriction). Workarounds:
1. Use `python3 -m yt_dlp --extractor-args "youtube:player_client=ios"` 
2. Use cookies from an authenticated browser session via `--cookies-from-browser chrome`
3. Try a different user-uploaded copy of the same audio

## Search and Download from YouTube Search

```bash
# Search and get video IDs
python3 -m yt_dlp "ytsearch5:query term" --flat-playlist --print "%(id)s %(title)s %(view_count)s"

# Download first result
python3 -m yt_dlp -x --audio-format mp3 "ytsearch1:artist song name"
```

## Verify Downloaded File

```bash
file ~/Downloads/filename.mp3
# Expected: "Audio file with ID3 version 2.x, contains: MPEG ADTS, layer III, v1, 64 kbps, 44.1 kHz, Stereo"
```

Note: Bitrate shown by `file` is the YouTube encode bitrate, not necessarily the max available. If only 64kbps shows for old/obscure uploads, the uploader only provided 360p video quality and the audio was heavily compressed.

## References

- `references/soulseek-setup.md` — Soulseek setup via Docker (slskd), Nicotine+ headless, or aioslsk. Use when a track isn't available in high quality on YouTube (old remixes, bootlegs, free releases taken down from streaming).

## Pitfalls

- **Low bitrate for old uploads**: Many YouTube uploads from 10+ years ago are 360p max with 44-64kbps audio. This is a YouTube limitation, not a download tool limitation — the source upload doesn't contain higher quality audio. All uploads of the same track will have the same quality because they're all re-uploads of the same low-quality source.
- **Format 18 is often the only option**: For old/obscure uploads, the `android` client may only expose format 18 (640x360, h264, 44k AAC audio). Combined audio+video files will be ~9-14MB for a 7-8 minute track. This is the source, not a download config issue.
- **Audio format on macOS**: `--audio-format mp3` uses ffmpeg to re-encode. If ffmpeg isn't installed, `brew install ffmpeg` first. The re-encode can't improve the original audio quality — it just converts container + codec.
- **403 with android client**: The warning about skipped formats means some high-quality streams are blocked but format 18 (combined) should still work. If format 18 also fails, try adding `--no-check-certificates` or using cookies: `--cookies-from-browser chrome`.
- **Search results are not all videos**: `ytsearch:query` returns YouTube's top results. Use more specific queries for better results.
- **Copyright takedowns**: Many remixes/free releases get taken down over time. The original upload may not exist anymore — check alternative uploads on YouTube or other platforms.
- **Soulseek alternative**: For tracks not available in high quality on YouTube (especially old remixes, bootlegs, free releases), Soulseek is the better option. See the `soulseek-setup` reference for the Docker + aioslsk setup.
