#!/usr/bin/env python3
"""将多张图片从上到下合并为一张图片。"""

import sys
from pathlib import Path
from PIL import Image


def merge_images_vertical(image_paths: list[str], output_path: str, align: str = "left") -> None:
    """
    将多张图片垂直拼接（从上到下）。

    Args:
        image_paths: 输入图片路径列表
        output_path: 输出图片路径
        align: 水平对齐方式，'left'、'center' 或 'right'
    """
    images = [Image.open(p) for p in image_paths]

    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    result = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 255))

    y_offset = 0
    for img in images:
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        if align == "center":
            x = (total_width - img.width) // 2
        elif align == "right":
            x = total_width - img.width
        else:
            x = 0

        result.paste(img, (x, y_offset))
        y_offset += img.height

    # 保存时根据格式决定是否保留透明通道
    out = Path(output_path)
    if out.suffix.lower() in (".jpg", ".jpeg"):
        result = result.convert("RGB")

    result.save(output_path)
    print(f"已保存到 {output_path}（{total_width}x{total_height}）")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="将多张图片从上到下合并为一张图片")
    parser.add_argument("images", nargs="+", help="输入图片路径（按顺序排列）")
    parser.add_argument("-o", "--output", default="merged.png", help="输出文件路径（默认：merged.png）")
    parser.add_argument(
        "--align",
        choices=["left", "center", "right"],
        default="left",
        help="宽度不一致时的水平对齐方式（默认：left）",
    )

    args = parser.parse_args()

    missing = [p for p in args.images if not Path(p).exists()]
    if missing:
        print(f"错误：找不到文件：{', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    merge_images_vertical(args.images, args.output, args.align)


if __name__ == "__main__":
    main()
