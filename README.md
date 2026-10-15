# 🌿 life-skills

个人日常生活、影音与自动化小工具集合。支持作为 AI Agent 的 Skills 扩展，亦可直接在本地终端作为独立 CLI 运行。

---

## 📦 已包含的 Skills

| Skill 名称 | 描述 | 触发示例 |
| :--- | :--- | :--- |
| **[`huavod-downloader`](./skills/huavod-downloader/)** | 流媒体/HLS 高清视频与剧集自动化检索、防验证解析、16 线程并发下载与 MP4 混流封装 | “我想看凡人修仙传动漫最新一集”<br>“帮我搜一下电影《希望》”<br>“把这个视频链接下载到本地” |
| **[`media-cast`](./skills/media-cast/)** | 局域网智能电视与投影仪自动发现（DLNA/UPnP），本地高速流媒体中继与大屏硬解播放控制 | “把刚才下载的视频投屏到电视”<br>“扫描家里有哪些投屏设备”<br>“暂停 / 继续 / 停止投屏” |

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
