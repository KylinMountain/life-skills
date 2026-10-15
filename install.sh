#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
SHARE_BIN_DIR="$HOME/.local/share/huavod-dl/bin"
SKILLS_DIR="$HOME/.gemini/config/skills"

mkdir -p "$BIN_DIR"
mkdir -p "$SHARE_BIN_DIR"
mkdir -p "$SKILLS_DIR"

# 1. 安装 CLI 工具
echo "Installing CLI utilities..."
if [ -f "$REPO_DIR/skills/huavod-downloader/scripts/huavod-dl" ]; then
    cp "$REPO_DIR/skills/huavod-downloader/scripts/huavod-dl" "$BIN_DIR/huavod-dl"
    chmod +x "$BIN_DIR/huavod-dl"
fi

if [ -f "$REPO_DIR/skills/media-cast/scripts/tv-cast" ]; then
    cp "$REPO_DIR/skills/media-cast/scripts/tv-cast" "$BIN_DIR/tv-cast"
    chmod +x "$BIN_DIR/tv-cast"
fi

# 2. 检查依赖引擎
ARCH="$(uname -m)"
OS="$(uname -s)"

if [ ! -f "$SHARE_BIN_DIR/N_m3u8DL-RE" ]; then
    if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
        curl -L -s "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-arm64_20260629.tar.gz" | tar -xz -C "$SHARE_BIN_DIR"
    elif [ "$OS" = "Darwin" ] && [ "$ARCH" = "x86_64" ]; then
        curl -L -s "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-x64_20260629.tar.gz" | tar -xz -C "$SHARE_BIN_DIR"
    fi
    chmod +x "$SHARE_BIN_DIR"/N_m3u8DL-RE* 2>/dev/null || true
fi

if [ ! -f "$SHARE_BIN_DIR/ffmpeg" ]; then
    if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
        curl -L -s "https://github.com/eugeneware/ffmpeg-static/releases/download/b6.1.1/ffmpeg-darwin-arm64.gz" | gunzip > "$SHARE_BIN_DIR/ffmpeg"
        chmod +x "$SHARE_BIN_DIR/ffmpeg"
    fi
fi

# 3. 注册技能
for skill_dir in "$REPO_DIR"/skills/*; do
    if [ -d "$skill_dir" ]; then
        skill_name="$(basename "$skill_dir")"
        target_dir="$SKILLS_DIR/$skill_name"
        rm -rf "$target_dir"
        mkdir -p "$target_dir"
        cp -R "$skill_dir"/* "$target_dir"/
    fi
done

echo "Done! CLI tools (huavod-dl, tv-cast) and skills installed."
