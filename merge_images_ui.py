#!/usr/bin/env python3
"""图片合并工具 - 图形界面"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk


class MergeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片合并工具")
        self.resizable(True, True)
        self.minsize(500, 400)

        self.image_paths: list[str] = []
        self.thumbnails: list[ImageTk.PhotoImage] = []  # 防止被GC

        self._build_ui()

    def _build_ui(self):
        # 顶部工具栏
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="添加图片", command=self._add_images).pack(side="left", padx=4)
        ttk.Button(toolbar, text="清空", command=self._clear).pack(side="left", padx=4)

        ttk.Label(toolbar, text="对齐方式：").pack(side="left", padx=(16, 4))
        self.align_var = tk.StringVar(value="left")
        for text, val in [("左", "left"), ("居中", "center"), ("右", "right")]:
            ttk.Radiobutton(toolbar, text=text, variable=self.align_var, value=val).pack(side="left")

        ttk.Button(toolbar, text="合并并保存", command=self._merge, style="Accent.TButton").pack(side="right", padx=4)

        # 图片列表区域
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.canvas = tk.Canvas(frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # 底部状态栏
        self.status_var = tk.StringVar(value="请添加图片")
        ttk.Label(self, textvariable=self.status_var, foreground="gray").pack(pady=(0, 6))

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _add_images(self):
        paths = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff"), ("所有文件", "*.*")],
        )
        for p in paths:
            if p not in self.image_paths:
                self.image_paths.append(p)
        self._refresh_list()

    def _clear(self):
        self.image_paths.clear()
        self._refresh_list()

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()

        for i, path in enumerate(self.image_paths):
            self._add_row(i, path)

        self.status_var.set(f"已选 {len(self.image_paths)} 张图片" if self.image_paths else "请添加图片")

    def _add_row(self, index: int, path: str):
        row = ttk.Frame(self.list_frame, padding=4)
        row.pack(fill="x", pady=2, padx=4)

        # 缩略图
        try:
            img = Image.open(path)
            img.thumbnail((64, 64))
            thumb = ImageTk.PhotoImage(img)
            self.thumbnails.append(thumb)
            ttk.Label(row, image=thumb).pack(side="left", padx=(0, 8))
        except Exception:
            ttk.Label(row, text="[?]", width=8).pack(side="left", padx=(0, 8))

        # 文件信息
        info_frame = ttk.Frame(row)
        info_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(info_frame, text=Path(path).name, font=("", 11, "bold")).pack(anchor="w")
        try:
            img = Image.open(path)
            ttk.Label(info_frame, text=f"{img.width}×{img.height}  {Path(path).suffix.upper()}", foreground="gray").pack(anchor="w")
        except Exception:
            pass

        # 操作按钮
        btn_frame = ttk.Frame(row)
        btn_frame.pack(side="right")
        ttk.Button(btn_frame, text="↑", width=3, command=lambda i=index: self._move(i, -1)).pack(side="left")
        ttk.Button(btn_frame, text="↓", width=3, command=lambda i=index: self._move(i, 1)).pack(side="left")
        ttk.Button(btn_frame, text="删除", command=lambda i=index: self._remove(i)).pack(side="left", padx=(4, 0))

        ttk.Separator(self.list_frame, orient="horizontal").pack(fill="x", padx=4)

    def _move(self, index: int, direction: int):
        new_index = index + direction
        if 0 <= new_index < len(self.image_paths):
            self.image_paths[index], self.image_paths[new_index] = (
                self.image_paths[new_index],
                self.image_paths[index],
            )
            self._refresh_list()

    def _remove(self, index: int):
        self.image_paths.pop(index)
        self._refresh_list()

    def _merge(self):
        if not self.image_paths:
            messagebox.showwarning("提示", "请先添加图片")
            return

        output_path = filedialog.asksaveasfilename(
            title="保存合并结果",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("所有文件", "*.*")],
        )
        if not output_path:
            return

        try:
            images = [Image.open(p) for p in self.image_paths]
            align = self.align_var.get()
            total_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)

            result = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 255))
            y = 0
            for img in images:
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                if align == "center":
                    x = (total_width - img.width) // 2
                elif align == "right":
                    x = total_width - img.width
                else:
                    x = 0
                result.paste(img, (x, y))
                y += img.height

            if Path(output_path).suffix.lower() in (".jpg", ".jpeg"):
                result = result.convert("RGB")
            result.save(output_path)

            messagebox.showinfo("完成", f"已保存到：\n{output_path}\n\n尺寸：{total_width}×{total_height}")
        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    app = MergeApp()
    app.mainloop()
