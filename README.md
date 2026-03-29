# 🧰 Handy Tools

一个开箱即用的在线工具箱，所有处理均在浏览器本地完成，文件不会上传到任何服务器。

**在线地址：** https://handy-tools-eda.pages.dev

## 工具列表

### 图片工具
| 工具 | 说明 |
|------|------|
| [图片合并](merge_images.html) | 将多张图片按行列网格拼接为一张，支持拖拽排序 |
| [图片压缩](compress.html) | 压缩 PNG / JPEG / WebP，可调整质量与尺寸 |
| [图片裁剪](crop.html) | 自由裁剪或按固定比例裁剪图片 |
| [调整尺寸](resize.html) | 批量修改图片宽高，支持保持长宽比 |
| [格式转换](convert.html) | PNG / JPEG / WebP 互相转换 |
| [添加水印](watermark.html) | 添加文字或图片水印，支持平铺和自由拖拽 |
| [去除水印](remove-watermark.html) | 通过涂抹区域去除图片水印 |

### 视频工具
| 工具 | 说明 |
|------|------|
| [提取音频](extract-audio.html) | 从视频文件中分离音轨并下载为 MP3 |

## Python 脚本

项目还包含两个图片合并的 Python 工具（需要安装 Pillow）：

```bash
pip install pillow

# 命令行版本：将多张图片垂直合并
python merge_images.py image1.png image2.png -o output.png --align center

# 图形界面版本
python merge_images_ui.py
```

## 本地运行

直接用浏览器打开任意 `.html` 文件即可，无需安装依赖或启动服务器。

## 部署

通过 GitHub Actions 自动部署到 Cloudflare Pages，每次推送到 `main` 分支即触发部署。
