# 🌿 life-skills

个人日常生活、影音与自动化小工具集合。支持作为 AI Agent 的 Skills 扩展，亦可直接在本地终端作为独立 CLI 运行。

---

## 🛠️ 已包含工具

- **`stream-downloader`（流媒体解析与本地缓存）**
  - 支持特定 HLS/m3u8 视频流解析、分片多线程极速拉取与断点重试。
  - 内置代理自动探测与调度，规避网络抖动。
  - 下载完成后自动通过 FFmpeg 无损混流封装为标准 `.mp4`。

---

## ⚡ 快速使用

### 1. 一键安装
```bash
git clone https://github.com/KylinMountain/life-skills.git
cd life-skills && ./install.sh
```

### 2. 命令行使用
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

---

## 📂 仓库结构

```text
life-skills/
├── skills/          # AI 智能体技能模块（适配通用 Agent Skills 规范）
│   └── huavod-downloader/
│       ├── SKILL.md
│       └── scripts/
│           └── huavod-dl
├── install.sh       # 环境初始化与依赖配置脚本
└── README.md
```

License: MIT
