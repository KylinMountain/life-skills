# 🌿 life-skills

个人日常生活、影音与自动化小工具集合。支持作为 AI Agent 的 Skills 扩展，亦可直接在本地终端作为独立 CLI 运行。

---

## 🛠️ 已包含工具 & Skills

### 1. `huavod-downloader`（流媒体解析与本地缓存）
- 支持特定 HLS/m3u8 视频流解析、分片多线程极速拉取与断点重试。
- 内置代理自动探测与调度，规避网络抖动。
- 下载完成后自动通过 FFmpeg 无损混流封装为标准 `.mp4`。

### 2. `media-cast`（局域网电视 / 投影仪智能投屏）
- 基于标准 DLNA / UPnP 协议，自动发现局域网内的智能电视（小米、索尼、海信、TCL等）与投影仪（极米、当贝等）。
- 本地启动轻量级支持 HTTP Range 的视频流媒体服务，实现电视端随意拖动进度、秒级缓冲与大屏硬解播放。
- 支持暂停、恢复、停止与播放进度查询。

---

## ⚡ 快速使用

### 1. 一键安装
```bash
git clone https://github.com/KylinMountain/life-skills.git
cd life-skills && ./install.sh
```

### 2. 命令行使用

#### 影视搜索与离线下载 (`huavod-dl`)
```bash
# 搜索资源
huavod-dl "<关键词>"

# 离线下载单片
huavod-dl "<视频链接>"

# 离线下载剧集指定集数（如第 1 到 5 集）
huavod-dl "<剧集链接>" --ep 1-5

# 仅解析 m3u8 流地址，不下载
huavod-dl "<视频链接>" --info
```

#### 局域网大屏投屏 (`tv-cast`)
```bash
# 扫描局域网内的可用电视与投影仪
tv-cast -l

# 一键投屏指定视频（单设备自动选中）
tv-cast "~/Downloads/希望.mp4"

# 投屏到指定设备（如存在多台设备时）
tv-cast "~/Downloads/希望.mp4" -d "Kylin的电视"

# 控制播放状态
tv-cast --pause    # 暂停
tv-cast --resume   # 恢复
tv-cast --status   # 查看进度
tv-cast --stop     # 停止投屏
```

---

## 📂 仓库结构

```text
life-skills/
├── skills/
│   ├── huavod-downloader/  # 视频流解析与下载 Skill
│   └── media-cast/         # 局域网智能投屏 Skill
├── install.sh              # 环境初始化与依赖配置脚本
└── README.md
```

License: MIT
