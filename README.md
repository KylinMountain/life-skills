# 🌟 Life Skills (日常实用与娱乐技能库)

日常个人生活、影音娱乐与自动化辅助专用的 **[Google Antigravity](https://github.com/google)** 技能库（Skills Collection）。

赋能 AI 智能体，让你只需要用自然语言说出需求，就能自动完成影视搜索、视频提取、切片下载、格式混流以及各类生活日常自动化任务。

---

## 📦 已包含的 Skills

| Skill 名称 | 描述 | 触发示例 |
| :--- | :--- | :--- |
| **[`huavod-downloader`](./skills/huavod-downloader/)** | 华视影院 / 华影网 (huavod.com) 专属高清视频/剧集自动化搜索、防倒计时解析、多线程下载与 MP4 混流封装 | “我想看凡人修仙传动漫最新一集”、“把这个电影链接下载到本地” |

---

## ⚡ 快速安装

克隆仓库并运行一键安装脚本（自动配置依赖环境与 Antigravity 全局技能）：

```bash
git clone https://github.com/KylinMountain/life-skills.git
cd life-skills
chmod +x install.sh
./install.sh
```

安装脚本会自动完成：
1. 安装专用命令行工具 `huavod-dl` 至 `~/.local/bin/`；
2. 自动配置底层的 `N_m3u8DL-RE` 高并发下载引擎与 `FFmpeg` 混流引擎；
3. 将技能无缝注册至 Antigravity 全局配置目录 `~/.gemini/config/skills/`。

---

## 🎬 Skill 演示：影视搜索与下载 (`huavod-downloader`)

### 1. 对话模式（自然语言即用）
在 Antigravity 聊天窗口中直接对助手说：
* 🔍 **搜索影视**：“*帮我搜一下《凡人修仙传》*” ➔ AI 会列出动漫版、特别篇、真人版及演职员信息。
* 📥 **下载单片**：“*帮我把 https://huavod.com/vodplay/202979-1-1.html 下载到本地*”
* 📺 **下载剧集**：“*我想看凡人修仙传动漫最新一集*” 或 “*下载这部剧的第 1-3 集*”

AI 会自动在后台执行代理加速、倒计时验证、16 线程高速下载并将切片无损合并为 `.mp4` 文件存入 `~/Downloads`。

---

### 2. 命令行模式（CLI 独立使用）
工具已自带全功能的命令行程序 `huavod-dl`：

```bash
# 搜索影视资源
huavod-dl "凡人修仙传"

# 下载单部电影
huavod-dl "https://huavod.com/vodplay/202979-1-1.html"

# 查看电视剧集列表
huavod-dl "https://huavod.com/voddetail/203704.html"

# 下载电视剧指定集数（如第 1 集）
huavod-dl "https://huavod.com/voddetail/203704.html" --ep 1

# 批量下载指定范围（如第 1 到 5 集）
huavod-dl "https://huavod.com/voddetail/203704.html" --ep 1-5

# 仅解析 m3u8 地址而不下载
huavod-dl "https://huavod.com/vodplay/202979-1-1.html" --info
```

---

## 🛠️ 底层特性

* **智能代理路由**：自动检测本机运行的代理（如 Clash 端口 `127.0.0.1:7890`），消除握手延迟。
* **防广告验证绕过**：自动在后台完成服务端强制要求的 20 秒广告验证倒计时，换取真实切片清单。
* **极速并发与重试**：基于 `N_m3u8DL-RE` 引擎开启 16 线程分片拉取，支持单分片异常重试（最多 10 次）。
* **无损混流封装**：下载完成后自动使用 `FFmpeg` 混流封装为标准 H.264/AAC 的 `.mp4` 文件，全平台播放器皆可硬解秒播。

---

## 🤝 持续更新与贡献

生活类技能库持续扩展中，欢迎提交 Issue 或 Pull Request 分享你的日常生活实用 Skill！

License: MIT
