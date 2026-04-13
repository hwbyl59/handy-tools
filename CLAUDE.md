# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Chinese-language browser toolbox ("在线工具箱") for media processing. All processing happens locally in the browser — no server uploads. Live at https://handy-tools-eda.pages.dev.

There are also two Python CLI/GUI scripts for image merging (require Pillow: `pip install pillow`).

## Architecture

Each HTML tool is a **self-contained single file** with inline CSS and JS — no build step, no bundler, no shared JS files. Open any `.html` directly in a browser.

All tools share the same CSS custom properties (`:root` variables: `--bg`, `--surface`, `--border`, `--primary`, etc.) and follow the same UI pattern: drop zone for file input → settings panel → preview → download via `URL.createObjectURL`.

### External dependencies (loaded via CDN)
- `extract-audio.html` uses [lamejs](https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js) for MP3 encoding
- `transcribe.html` uses [Transformers.js](https://cdn.jsdelivr.net/npm/@xenova/transformers) + Whisper model (downloaded from Hugging Face on first use)

### index.html category structure
The landing page organizes tools into 4 categories: 图片工具 (image), 音频工具 (audio), 视频工具 (video), 文本工具 (text). Each category has a `<span class="category-count">` showing "X / Y 可用". Many tool slots are placeholder cards with `class="coming-soon"`.

## Deployment

Pushing to `main` auto-deploys to Cloudflare Pages via GitHub Actions (`.github/workflows/deploy.yml`). Uses `wrangler pages deploy .` — the entire repo root is the publish directory. Requires `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repo secrets.

## Adding a New Tool
1. Create `toolname.html` as a self-contained file reusing the existing CSS variable system
2. Add a `<a href="toolname.html" class="tool-card">` entry in `index.html` under the appropriate category section (replacing a `coming-soon` placeholder if one exists, or adding a new card)
3. Update that category's `<span class="category-count">` to reflect the new available/total count
4. All UI text should be in Chinese to match the existing tools
