---
name: youtube-transcript-fetch
description: "Fetch and analyze YouTube video transcripts for any channel. Uses youtube-transcript-api to extract full video text, then analyzes for key topics. Saves transcript for later reference."
---

# YouTube Transcript Fetcher

Fetch transcripts from YouTube videos for analysis, summarization, or research.

## Prerequisites

```bash
pip3 install youtube-transcript-api
```

## Usage

```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

# Fetch transcript
transcript = api.fetch("VIDEO_ID")

# Extract text
text = ' '.join([s.text for s in transcript.snippets])
duration_mins = int((snippets[-1].start + snippets[-1].duration) / 60)
```

## Finding Video IDs

From a channel page, use browser console:
```javascript
const links = document.querySelectorAll('a[href*="/watch?v="]');
const results = [];
links.forEach((l, i) => {
    results.push({index: i, title: l.textContent.trim(), url: l.href});
});
JSON.stringify(results);
```

## Analysis Workflow

1. Fetch transcript using `api.fetch(video_id)`
2. Read the full text - look for key topics, demonstrations, dashboards
3. Extract specific sections using text search
4. Save transcripts to /tmp for reference
5. Summarize findings with timestamps

## Pitfalls

- API version changed: `get_transcript` is now `fetch()` as an instance method
- `YouTubeTranscriptApi().fetch(video_id)` - must instantiate first
- Transcript object has `.snippets` property (list of FetchedTranscriptSnippet)
- Each snippet has `.text`, `.start`, `.duration` attributes
- Some videos have transcripts disabled — handle gracefully
