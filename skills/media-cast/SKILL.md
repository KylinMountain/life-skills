---
name: media-cast
description: Specialized skill for discovering local smart TVs, projectors, and casting local video files or streams to the big screen via DLNA/UPnP. Triggers when the user asks to cast a video to TV/projector or mentions "投屏", "放电视上", "大屏播放".
---

# Media Cast Skill

Enables the AI agent to discover smart TVs and projectors on the local Wi-Fi network and cast downloaded or local videos directly to the big screen.

---

## Tooling

Backed by the standalone CLI tool [`tv-cast`](file:///Users/evilkylin/.local/bin/tv-cast) (located in `~/.local/bin/tv-cast`):
- **Protocol**: Standard DLNA / UPnP AVTransport (supported by Xiaomi, Hisense, TCL, Sony, Dangbei, Xgimi, Apple TV with DLNA, etc.).
- **Streaming**: Lightweight background HTTP streaming server with HTTP 206 Range support (enables smooth buffering, seeking, and timeline control on the TV).

---

## Workflows

### 1. Discover Available Screens
When the user asks what TVs or projectors are available:
```bash
tv-cast -l --json
```
Present the found devices (Name, Manufacturer, IP).

### 2. Cast a Video
When the user says "把刚才下载的视频投屏" or "投屏到电视":
1. Check the target video file path (e.g. in `~/Downloads`).
2. Run casting command:
   ```bash
   tv-cast "<视频文件路径>"
   # Or specify device if multiple devices exist:
   tv-cast "<视频文件路径>" -d "<设备名或IP>"
   ```
3. Report success: video title, target TV name, and reminder of playback control commands.

### 3. Playback Controls
- **Pause**: `tv-cast --pause`
- **Resume**: `tv-cast --resume`
- **Stop**: `tv-cast --stop`
- **Status & Progress**: `tv-cast --status`
