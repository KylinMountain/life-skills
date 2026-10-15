#!/usr/bin/env bash
set -e

# Life Skills Installer for Antigravity & macOS / Linux
# Repository: https://github.com/KylinMountain/life-skills

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
SHARE_BIN_DIR="$HOME/.local/share/huavod-dl/bin"
SKILLS_DIR="$HOME/.gemini/config/skills"

echo "=================================================="
echo "  🌟 安装 Life Skills (生活日常实用技能集合)      "
echo "=================================================="

mkdir -p "$BIN_DIR"
mkdir -p "$SHARE_BIN_DIR"
mkdir -p "$SKILLS_DIR"

# 1. 安装 huavod-downloader CLI
echo "[1/3] 安装 huavod-dl 命令行工具到 $BIN_DIR ..."
cp "$REPO_DIR/skills/huavod-downloader/scripts/huavod-dl" "$BIN_DIR/huavod-dl"
chmod +x "$BIN_DIR/huavod-dl"

# 2. 检查并准备底层音视频下载依赖引擎
echo "[2/3] 检查底层依赖 (N_m3u8DL-RE & FFmpeg) ..."
ARCH="$(uname -m)"
OS="$(uname -s)"

if [ ! -f "$SHARE_BIN_DIR/N_m3u8DL-RE" ]; then
    echo "  -> 正在下载 N_m3u8DL-RE 引擎 ($OS $ARCH) ..."
    if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
        curl -L -s "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-arm64_20260629.tar.gz" | tar -xz -C "$SHARE_BIN_DIR"
    elif [ "$OS" = "Darwin" ] && [ "$ARCH" = "x86_64" ]; then
        curl -L -s "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-x64_20260629.tar.gz" | tar -xz -C "$SHARE_BIN_DIR"
    else
        echo "  [提示] 请自行在 $SHARE_BIN_DIR 放置适用于你系统的 N_m3u8DL-RE 可执行文件。"
    fi
    chmod +x "$SHARE_BIN_DIR"/N_m3u8DL-RE* 2>/dev/null || true
fi

if [ ! -f "$SHARE_BIN_DIR/ffmpeg" ]; then
    echo "  -> 正在下载 FFmpeg 引擎 ($OS $ARCH) ..."
    if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
        curl -L -s "https://github.com/eugeneware/ffmpeg-static/releases/download/b6.1.1/ffmpeg-darwin-arm64.gz" | gunzip > "$SHARE_BIN_DIR/ffmpeg"
        chmod +x "$SHARE_BIN_DIR/ffmpeg"
    fi
fi

# 3. 注册 Skill 到 Antigravity 全局技能目录
echo "[3/3] 注册 Skills 到 Antigravity ($SKILLS_DIR) ..."
for skill_dir in "$REPO_DIR"/skills/*; do
    if [ -d "$skill_dir" ]; then
        skill_name="$(basename "$skill_dir")"
        target_dir="$SKILLS_DIR/$skill_name"
        echo "  -> 链接技能: $skill_name"
        rm -rf "$target_dir"
        mkdir -p "$target_dir"
        cp -R "$skill_dir"/* "$target_dir"/
    fi
done

echo ""
echo "=================================================="
echo "  🎉 安装成功！"
echo "  - CLI 工具: huavod-dl (输入 huavod-dl --help 查看)"
echo "  - Antigravity: 已激活 huavod-downloader 技能"
echo "=================================================="
