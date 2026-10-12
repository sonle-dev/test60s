"""
GIAO DIEN DO HOA (GUI) - XU LY ANH TONG HOP
Ngon ngu: Python
Giao dien: Tkinter + Matplotlib Canvas
Xu ly anh: OpenCV, NumPy
"""

import os
import sys
import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class HistogramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ung Dung Xu Ly Anh & Histogram 3 Kenh Mau")
        self.root.geometry("1100, 720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#f1f5f9")

        self.current_image_path = None
        self.img_bgr = None
        self.img_rgb = None

        self.setup_ui()

        if os.path.exists("cat_input.jpg"):
            self.load_image_from_path("cat_input.jpg")
        elif os.path.exists("sample.jpg"):
            self.load_image_from_path("sample.jpg")

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1e293b", height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="HE THONG XU LY ANH & HISTOGRAM 3 KENH MAU (RGB)",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        # Control Bar
        control_frame = tk.Frame(self.root, bg="#e2e8f0", height=50)
        control_frame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=(10, 5))

        btn_select = tk.Button(
            control_frame,
            text="Chon Anh Input...",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.choose_image
        )
        btn_select.pack(side=tk.LEFT, padx=10, pady=6)

        btn_save = tk.Button(
            control_frame,
            text="Luu Ket Qua...",
            font=("Segoe UI", 10),
            bg="#10b981",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.save_figure
        )
        btn_save.pack(side=tk.LEFT, padx=5, pady=6)

        self.lbl_info = tk.Label(
            control_frame,
            text="Chua chon anh.",
            font=("Segoe UI", 10),
            bg="#e2e8f0",
            fg="#334155"
        )
        self.lbl_info.pack(side=tk.LEFT, padx=15, pady=6)

        # Content Frame
        content_frame = tk.Frame(self.root, bg="#f1f5f9")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Cot Trai: Input
        left_card = tk.LabelFrame(
            content_frame,
            text=" [INPUT] ANH GOC ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#0f172a",
            padx=10,
            pady=10
        )
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.canvas_image = tk.Canvas(left_card, bg="#f8fafc", highlightthickness=0)
        self.canvas_image.pack(fill=tk.BOTH, expand=True)

        # Cot Phai: Histogram Output
        right_card = tk.LabelFrame(
            content_frame,
            text=" [OUTPUT] HISTOGRAM 3 KENH MAU ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#0f172a",
            padx=5,
            pady=5
        )
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        self.fig = Figure(figsize=(6, 5), dpi=95, facecolor="white")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#fafafa")

        self.canvas_hist = FigureCanvasTkAgg(self.fig, master=right_card)
        self.canvas_hist.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar_frame = tk.Frame(right_card, bg="white")
        toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas_hist, toolbar_frame)
        self.toolbar.update()

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Chon anh dau vao",
            filetypes=[
                ("Hinh anh", "*.jpg;*.jpeg;*.png;*.bmp;*.webp;*.tiff"),
                ("Tat ca tap tin", "*.*")
            ]
        )
        if file_path:
            self.load_image_from_path(file_path)

    def load_image_from_path(self, file_path):
        try:
            with open(file_path, "rb") as f:
                bytes_data = bytearray(f.read())
                numpy_array = np.asarray(bytes_data, dtype=np.uint8)
                img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

            if img is None:
                messagebox.showerror("Loi", "Khong the doc file anh nay!")
                return

            self.current_image_path = file_path
            self.img_bgr = img
            self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h, w, c = self.img_bgr.shape
            filename = os.path.basename(file_path)
            self.lbl_info.config(text=f"Tep: {filename} | Kich thuoc: {w}x{h} px | Kenh mau: {c}")

            self.render_input_image()
            self.render_histogram()

        except Exception as e:
            messagebox.showerror("Loi", f"Co loi xay ra: {str(e)}")

    def render_input_image(self):
        if self.img_rgb is None:
            return

        self.root.update_idletasks()
        cw = self.canvas_image.winfo_width()
        ch = self.canvas_image.winfo_height()
        if cw < 50: cw = 450
        if ch < 50: ch = 450

        pil_img = Image.fromarray(self.img_rgb)
        img_w, img_h = pil_img.size
        ratio = min(cw / img_w, ch / img_h, 1.0)
        new_w = max(1, int(img_w * ratio))
        new_h = max(1, int(img_h * ratio))

        resized = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_photo = ImageTk.PhotoImage(resized)

        self.canvas_image.delete("all")
        self.canvas_image.create_image(cw // 2, ch // 2, image=self.tk_photo, anchor=tk.CENTER)

    def render_histogram(self):
        if self.img_bgr is None:
            return

        self.ax.clear()
        channels = ('b', 'g', 'r')
        colors = ('#2563eb', '#16a34a', '#dc2626')
        labels = ('Blue', 'Green', 'Red')

        for i, col in enumerate(channels):
            hist = cv2.calcHist([self.img_bgr], [i], None, [256], [0, 256])
            self.ax.plot(hist, color=colors[i], label=labels[i], linewidth=2, alpha=0.9)
            self.ax.fill_between(range(256), 0, hist.flatten(), color=colors[i], alpha=0.1)

        self.ax.set_title("Phan bo cuong do 3 kenh mau (0 - 255)", fontsize=11, fontweight='bold', color='#1e293b')
        self.ax.set_xlabel("Muc sang pixel (0 - 255)", fontsize=10)
        self.ax.set_ylabel("So luong pixel", fontsize=10)
        self.ax.set_xlim([0, 256])
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.legend(loc='upper right', fontsize=9, frameon=True)

        self.fig.tight_layout()
        self.canvas_hist.draw()

    def save_figure(self):
        if self.img_bgr is None:
            messagebox.showwarning("Canh bao", "Vui long chon anh truoc khi luu!")
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")],
            initialfile="histogram_output.png"
        )
        if out_path:
            self.fig.savefig(out_path, dpi=200, bbox_inches='tight')
            messagebox.showinfo("Thanh cong", f"Da luu bieu do vao:\n{out_path}")


def main():
    root = tk.Tk()
    app = HistogramApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
