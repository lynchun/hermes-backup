# Bloomberg RSS Feed — Working Alternative to Bot-Blocked Website

Bloomberg.com blocks automated access with a CAPTCHA challenge. However, their RSS feed is fully open and returns structured article data.

## Feed URL

```
https://feeds.bloomberg.com/markets/news.rss
```

## Returns

- `<title>` — Article headline
- `<description>` — 1-2 sentence summary
- `<link>` — Full article URL (may still hit paywall)
- `<pubDate>` — Publication date
- `<dc:creator>` — Author(s)
- `<media:content>` — Thumbnail image

## Example Output

```
Title: Oil Holds Decline as Traders See Progress Toward Iranian Deal
Description: Oil held a drop on signs that negotiations to extend a US-Iranian
  ceasefire and reopen the Strait of Hormuz were making progress.
Published: Mon, 25 May 2026 22:07:49 GMT
Link: https://www.bloomberg.com/news/articles/2026-05-25/latest-oil-market-news-and-analysis-for-may-26
```

## Comparison

| Approach | Works? |
|----------|--------|
| Browser to bloomberg.com | No — Captcha |
| Bloomberg RSS feed | Yes — full data |
| Google News RSS for bloomberg.com | Yes — fallback |

## Other RSS Feeds That Work

Google News RSS bypasses bot blocks for any source:
- **Reuters**: `https://news.google.com/rss/search?q=site:reuters.com`
- **ZeroHedge**: `https://news.google.com/rss/search?q=site:zerohedge.com`
