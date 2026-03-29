# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A collection of client-side browser tools (Chinese-language "toolbox") for media processing. All processing happens locally in the browser — no server uploads. There are also two Python CLI/GUI scripts for image merging.

## Running the Tools

Open any `.html` file directly in a browser. No build step, no package manager, no server required for current tools. Future tools may introduce a backend.

For the Python scripts:
```bash
# CLI: merge images vertically
python merge_images.py image1.png image2.png -o output.png --align center

# GUI: tkinter-based image merge tool
python merge_images_ui.py
```

The Python scripts require Pillow (`pip install pillow`).

## Architecture

### HTML Tools (standalone single-file apps)
Each tool is a self-contained HTML file with inline CSS and JS. They share a consistent design system via CSS custom properties defined in `:root` (same variables across all files: `--bg`, `--surface`, `--border`, `--primary`, etc.).

- `index.html` — landing page with tool cards and category navigation
- `compress.html` — image compression via Canvas API (`toBlob`)
- `crop.html` — image cropping
- `resize.html` — batch image resize
- `convert.html` — PNG/JPEG/WebP format conversion
- `merge_images.html` — grid-based image merging with drag-to-reorder
- `watermark.html` — add text/image watermarks (tile or free-drag modes)
- `remove-watermark.html` — inpainting-style watermark removal using Canvas pixel manipulation
- `extract-audio.html` — extract audio from video using Web Audio API + [lamejs](https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js) for MP3 encoding

### Common UI patterns across HTML tools
- Drop zone + file input for drag-and-drop or click-to-select
- Settings panel (hidden until files are loaded)
- Side-by-side before/after preview
- Download via `URL.createObjectURL` + `<a>.click()`
- `URL.revokeObjectURL` for memory cleanup
- `canvas` element (hidden) used as processing surface

### Python scripts
- `merge_images.py` — CLI using Pillow, vertical stacking with left/center/right alignment
- `merge_images_ui.py` — tkinter GUI wrapping the same logic with thumbnail preview list

## Adding a New Tool
1. Create `toolname.html` as a self-contained file following the existing CSS variable system
2. Add a tool card entry in `index.html` under the appropriate category section
3. Update the category `<span class="category-count">` to reflect the new count
