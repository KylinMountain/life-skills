---
name: huavod-downloader
description: Specialized skill for searching, resolving, and downloading HLS media streams to local MP4 format. Triggers when the user asks to search or download media links from huavod or requests offline playback for supported streams.
---

# Stream Downloader Skill

Enables the AI agent to search, parse, and download video streams directly to the local disk in `.mp4` format.

---

## Capabilities

Backed by the local CLI [`huavod-dl`](file:///Users/evilkylin/.local/bin/huavod-dl) (located in `~/.local/bin/huavod-dl`):
- **Search**: Find resources by keyword.
- **Parse & Resolve**: Bypasses countdown verification and fetches the underlying `.m3u8` playlist.
- **Concurrent Download**: 16-thread segment fetching via `N_m3u8DL-RE`.
- **Remux**: Remuxes into standard `.mp4` via `ffmpeg`.

---

## Usage Patterns

### 1. Search
```bash
huavod-dl -s "<keyword>" --json
```

### 2. Download Movie or Single Episode
```bash
huavod-dl "<URL>"
```

### 3. Download Drama / Series Episodes
```bash
huavod-dl "<DETAIL_URL>" --ep 1
huavod-dl "<DETAIL_URL>" --ep 1-5
huavod-dl "<DETAIL_URL>" --ep all
```

### 4. Inspect Stream URL
```bash
huavod-dl "<URL>" --info
```
