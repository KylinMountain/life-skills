---
name: huavod-downloader
description: Comprehensive skill for searching, parsing, extracting, and downloading high-definition movies and TV series from huavod.com (华视影院 / 华影网). Activate this skill whenever the user asks to search for or download any movie, anime, TV series, or video from huavod, or provides a huavod URL (vodplay or voddetail) or says "我想看/我想搜/帮我下载 [片名]".
---

# HuaVod Video Search & Downloader Skill

This skill enables Antigravity to search, query, parse, and download movies, TV series, anime, and variety shows from `huavod.com` (华视影院 / 华影网) directly to the user's local disk in standard, playable `.mp4` format.

---

## Architecture & Underlying Tools

The system uses a standalone CLI utility [`huavod-dl`](file:///Users/evilkylin/.local/bin/huavod-dl) (located in `~/.local/bin/huavod-dl`), backed by:
- **Download Engine**: `N_m3u8DL-RE` (in `~/.local/share/huavod-dl/bin/N_m3u8DL-RE`)
- **Remux Engine**: `ffmpeg` (in `~/.local/share/huavod-dl/bin/ffmpeg`)
- **Network Acceleration**: Automatically connects through local Clash proxy (`127.0.0.1:7890`) or system proxy if present to bypass Cloudflare latency.

---

## Agent Workflows

### 1. Natural Language Search Workflow ("我想看/我想搜...")
When the user says "我想看凡人修仙传" or "帮我搜一下电影《希望》":
1. Run the search command with `--json` for structured results:
   ```bash
   huavod-dl -s "<关键词>" --json
   ```
2. Present the matched results clearly to the user:
   - Title & update status (e.g. `凡人修仙传 [更新至195集]`)
   - Category / Year / Region (e.g. `2020 / 大陆 / 国产动漫`)
   - Main actors / cast
   - Associated Detail URL
3. If unambiguous or if the user specified a single result, ask or proceed to download the requested episode(s).

### 2. Video Download Workflow

#### Case A: Movie or Single Episode Play URL
Format: `https://huavod.com/vodplay/<id>-<sid>-<nid>.html`
Run:
```bash
huavod-dl "<URL>"
```
- The script automatically waits for the ~20s server-side pre-roll ad verification countdown.
- 16 parallel threads download the unencrypted TS segments.
- Automatically remuxes into a single `.mp4` file in `~/Downloads/<Title>.mp4`.

#### Case B: Multi-Episode TV Series (Detail URL)
Format: `https://huavod.com/voddetail/<id>.html`
1. **Query available episodes first**:
   ```bash
   huavod-dl "<DETAIL_URL>"
   ```
2. **Download specified episode(s)** based on user request:
   - Single episode: `huavod-dl "<DETAIL_URL>" --ep 1`
   - Episode range: `huavod-dl "<DETAIL_URL>" --ep 1-5`
   - Selected list: `huavod-dl "<DETAIL_URL>" --ep 1,3,7`
   - Whole season: `huavod-dl "<DETAIL_URL>" --ep all`

#### Case C: Inspect Stream Without Downloading
When the user just wants the m3u8 playlist URL or media metadata:
```bash
huavod-dl "<URL>" --info
# Or JSON output:
huavod-dl "<URL>" --json
```

---

## Command Reference

| Command | Description |
| :--- | :--- |
| `huavod-dl "<关键词>"` | 搜索影片/剧集并展示列表与链接 |
| `huavod-dl -s "<关键词>" --json` | 搜索并以标准 JSON 输出匹配列表 |
| `huavod-dl "<url>"` | 下载单部电影或单集视频至 `~/Downloads` |
| `huavod-dl "<detail_url>"` | 查看电视剧所有可选集数 |
| `huavod-dl "<detail_url>" --ep <N>` | 下载电视剧第 N 集 |
| `huavod-dl "<detail_url>" --ep all` | 下载电视剧全集 |
| `huavod-dl "<url>" -o <DIR>` | 指定自定义输出目录 |
| `huavod-dl "<url>" -t <THREADS>` | 设置并发下载线程数（默认: 16） |
| `huavod-dl "<url>" --info` | 仅提取 M3U8 真实流地址与元数据，不执行下载 |

---

## Verification & Post-Download

After the download finishes:
1. Check that the output file exists in `~/Downloads/<Title>.mp4`.
2. Report the final video file path, file size (MB/GB), and video duration to the user.
