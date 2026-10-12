"""
CHUONG TRINH XU LY ANH TONG HOP (NOP BAI)
Bao gom:
1. Histogram 3 mau (RGB)
2. Tang va Giam do tuong phan
3. Can bang Histogram (Histogram Equalization) & Bieu do sau can bang
4. Tach nguong (Otsu Thresholding)
5. Anh am ban (Negative)
6. Cong anh (Addition)
7. Tru anh (Subtraction)
Hien thi tat ca ket qua chung tren 1 khung nhin va tu dong luu file anh nop bai.
Ho tro moi dinh dang anh (JPG, PNG, JPEG, BMP, WEBP...), moi kich thuoc, moi ten file.
"""

import os
import sys
import urllib.request
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


def read_image_safely(image_source: str):
    """
    Doc anh an toan cho moi dinh dang anh va moi loai duong dan:
    - Ho tro duong dan tieng Viet co dau, khoang trang, ky tu dac biet
    - Ho tro ca duong dan online (URL)
    - Xu ly tu dong anh xam (Gray), anh trong suot (RGBA) -> Chuyen ve 3 kenh BGR chuan
    """
    clean_path = image_source.strip().strip('"').strip("'")

    if clean_path.startswith("http://") or clean_path.startswith("https://"):
        try:
            print(f"[*] Dang tai anh tu internet: {clean_path} ...")
            req = urllib.request.Request(clean_path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                image_bytes = np.asarray(bytearray(resp.read()), dtype=np.uint8)
                img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"[!] Loi khi tai anh tu URL: {e}")
            return None
    else:
        norm_path = os.path.normpath(clean_path)
        if not os.path.exists(norm_path):
            return None
        try:
            # Doc file nhi phan roi decode giup tranh 100% loi ky tu Unicode tieng Viet tren Windows
            with open(norm_path, "rb") as f:
                bytes_data = bytearray(f.read())
                numpy_array = np.asarray(bytes_data, dtype=np.uint8)
                img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"[!] Loi khi doc file anh: {e}")
            return None

    if img is None:
        return None

    # Chuan hoa ve dung 3 kenh mau BGR de bat ky anh nao cung xu ly duoc khong bi loi
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    return img


def select_image_file():
    """Mo hop thoai cho phep chon bat ky file anh nao tu may tinh."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Chon anh tai len",
        filetypes=[
            ("Dinh dang anh pho bien", "*.jpg;*.jpeg;*.png;*.bmp;*.webp;*.tiff"),
            ("Tat ca tap tin", "*.*")
        ]
    )
    root.destroy()
    return file_path if file_path else None


def find_any_existing_image():
    """Tu dong tim 1 file anh co san trong thu muc lam fallback."""
    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
    for file in os.listdir('.'):
        lower_file = file.lower()
        if lower_file.endswith(supported_exts) and not lower_file.startswith('ket_qua') and not lower_file.startswith('output'):
            return file
    return None


def create_second_image(h, w):
    """
    Tao anh thu 2 dong kich thuoc voi anh input bat ky de thuc hien phep cong va tru anh.
    """
    img2 = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            img2[y, x, 0] = int(120 * (x / w))
            img2[y, x, 1] = int(120 * (y / h))
            img2[y, x, 2] = int(100 * ((x + y) / (w + h)))
    center_x, center_y = w // 2, h // 2
    radius = max(5, min(h, w) // 4)
    cv2.circle(img2, (center_x, center_y), radius, (180, 180, 180), -1)
    cv2.rectangle(img2, (w // 8, h // 8), (max(w // 8 + 10, w // 3), max(h // 8 + 10, h // 3)), (80, 150, 220), -1)
    return img2


def process_and_display_all(image_path: str, save_output=True):
    """
    Thuc hien tat ca cac phep toan xu ly anh va hien thi chung tren 1 giao dien nop bai.
    Ho tro moi anh, khong phu thuoc bat ky ten anh co dinh nao.
    """
    img_bgr = read_image_safely(image_path)

    if img_bgr is None:
        print(f"[!] Khong the doc file anh tai: {image_path}")
        return False

    h, w, c = img_bgr.shape
    print(f"\n[+] Xu ly anh thanh cong: Kich thuoc {w}x{h} px, {c} kenh mau")

    # 1. Anh goc RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 2. Tang va Giam do tuong phan
    img_contrast_high = cv2.convertScaleAbs(img_bgr, alpha=1.6, beta=10)
    img_contrast_low = cv2.convertScaleAbs(img_bgr, alpha=0.5, beta=30)
    img_contrast_high_rgb = cv2.cvtColor(img_contrast_high, cv2.COLOR_BGR2RGB)
    img_contrast_low_rgb = cv2.cvtColor(img_contrast_low, cv2.COLOR_BGR2RGB)

    # 3. Can bang Histogram tren khong gian mau YCrCb
    img_ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    channels_ycrcb = list(cv2.split(img_ycrcb))
    channels_ycrcb[0] = cv2.equalizeHist(channels_ycrcb[0])
    img_equalized_ycrcb = cv2.merge(channels_ycrcb)
    img_equalized_bgr = cv2.cvtColor(img_equalized_ycrcb, cv2.COLOR_YCrCb2BGR)
    img_equalized_rgb = cv2.cvtColor(img_equalized_bgr, cv2.COLOR_BGR2RGB)

    # 4. Tach nguong Otsu
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    otsu_threshold_value, img_threshold = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # 5. Anh am ban (Negative)
    img_negative_bgr = cv2.bitwise_not(img_bgr)
    img_negative_rgb = cv2.cvtColor(img_negative_bgr, cv2.COLOR_BGR2RGB)

    # 6. Tao anh 2 va thuc hien Cong anh, Tru anh
    img2_bgr = create_second_image(h, w)
    img2_rgb = cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2RGB)
    img_add_bgr = cv2.add(img_bgr, img2_bgr)
    img_add_rgb = cv2.cvtColor(img_add_bgr, cv2.COLOR_BGR2RGB)
    img_sub_bgr = cv2.absdiff(img_bgr, img2_bgr)
    img_sub_rgb = cv2.cvtColor(img_sub_bgr, cv2.COLOR_BGR2RGB)

    # =========================================================================
    # VE VA HIEN THI CHUNG TAT CA TREN 1 CUA SO (3 HANG x 4 COT)
    # =========================================================================
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(3, 4, figsize=(20, 13), dpi=100)
    fig.canvas.manager.set_window_title("KET QUA XU LY ANH")

    # O 1: Anh goc Input (Tong quat, khong bi rang buoc ten anh)
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title(f"1. Anh Goc Input ({w}x{h})", fontsize=11, fontweight='bold', color='#0f172a')
    axes[0, 0].axis('off')

    # O 2: Histogram 3 mau RGB (Input)
    colors = ('blue', 'green', 'red')
    labels = ('Blue', 'Green', 'Red')
    for i, col in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist([img_bgr], [i], None, [256], [0, 256])
        axes[0, 1].plot(hist, color=colors[i], label=labels[i], linewidth=1.8, alpha=0.85)
        axes[0, 1].fill_between(range(256), 0, hist.flatten(), color=colors[i], alpha=0.1)
    axes[0, 1].set_title("2. Histogram 3 Mau (RGB)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[0, 1].set_xlim([0, 256])
    axes[0, 1].set_xlabel("Muc sang (0 - 255)", fontsize=9)
    axes[0, 1].set_ylabel("So pixel", fontsize=9)
    axes[0, 1].legend(loc='upper right', fontsize=8)
    axes[0, 1].grid(True, linestyle='--', alpha=0.5)

    # O 3: Tang do tuong phan
    axes[0, 2].imshow(img_contrast_high_rgb)
    axes[0, 2].set_title("3. Tang Tuong Phan (alpha=1.6)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[0, 2].axis('off')

    # O 4: Giam do tuong phan
    axes[0, 3].imshow(img_contrast_low_rgb)
    axes[0, 3].set_title("4. Giam Tuong Phan (alpha=0.5)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[0, 3].axis('off')

    # O 5: Can bang Histogram
    axes[1, 0].imshow(img_equalized_rgb)
    axes[1, 0].set_title("5. Can Bang Histogram", fontsize=11, fontweight='bold', color='#0f172a')
    axes[1, 0].axis('off')

    # O 6: Histogram sau can bang
    for i, col in enumerate(('b', 'g', 'r')):
        hist_eq = cv2.calcHist([img_equalized_bgr], [i], None, [256], [0, 256])
        axes[1, 1].plot(hist_eq, color=colors[i], label=labels[i], linewidth=1.8, alpha=0.85)
        axes[1, 1].fill_between(range(256), 0, hist_eq.flatten(), color=colors[i], alpha=0.1)
    axes[1, 1].set_title("6. Histogram Sau Can Bang", fontsize=11, fontweight='bold', color='#0f172a')
    axes[1, 1].set_xlim([0, 256])
    axes[1, 1].set_xlabel("Muc sang (0 - 255)", fontsize=9)
    axes[1, 1].set_ylabel("So pixel", fontsize=9)
    axes[1, 1].legend(loc='upper right', fontsize=8)
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    # O 7: Tach nguong Otsu
    axes[1, 2].imshow(img_threshold, cmap='gray')
    axes[1, 2].set_title(f"7. Tach Nguong Otsu (Nguong={int(otsu_threshold_value)})", fontsize=11, fontweight='bold', color='#0f172a')
    axes[1, 2].axis('off')

    # O 8: Anh am ban (Negative)
    axes[1, 3].imshow(img_negative_rgb)
    axes[1, 3].set_title("8. Anh Am Ban (Negative)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[1, 3].axis('off')

    # O 9: Anh phu (Image 2)
    axes[2, 0].imshow(img2_rgb)
    axes[2, 0].set_title("9. Anh Thu 2 (Mau Ket Hop)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[2, 0].axis('off')

    # O 10: Cong anh
    axes[2, 1].imshow(img_add_rgb)
    axes[2, 1].set_title("10. Cong Anh (Anh 1 + Anh 2)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[2, 1].axis('off')

    # O 11: Tru anh
    axes[2, 2].imshow(img_sub_rgb)
    axes[2, 2].set_title("11. Tru Anh (|Anh 1 - Anh 2|)", fontsize=11, fontweight='bold', color='#0f172a')
    axes[2, 2].axis('off')

    # O 12: Bang thong so xu ly (Tong quat, khong loi font)
    axes[2, 3].axis('off')
    mean_val = np.mean(img_gray)
    std_val = np.std(img_gray)
    min_val = np.min(img_gray)
    max_val = np.max(img_gray)

    info_text = (
        f"--- THONG SO XU LY ANH ---\n\n"
        f"- Anh dau vao: Image Input\n"
        f"- Do phan giai: {w} x {h} px\n"
        f"- So kenh mau: {c} (RGB)\n"
        f"- Do sang TB (Mean): {mean_val:.2f}\n"
        f"- Do lech chuan (Std): {std_val:.2f}\n"
        f"- Min - Max: {min_val} - {max_val}\n"
        f"- Nguong Otsu: {int(otsu_threshold_value)}\n"
        f"- Phep cong: cv2.add (Bao hoa 255)\n"
        f"- Phep tru: cv2.absdiff (Tri tuyet doi)\n"
        f"- Can bang: cv2.equalizeHist (Kenh Y)\n"
    )
    axes[2, 3].text(
        0.05, 0.5, info_text, fontsize=11, verticalalignment='center',
        bbox=dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1.5)
    )

    plt.tight_layout()

    # Luu file ket qua nop bai
    if save_output:
        output_file = "ket_qua_nop_bai.png"
        plt.savefig(output_file, dpi=160, bbox_inches='tight')
        print(f"[+] DA XUAT FILE KET QUA: {output_file}")

    print("[+] Dang mo cua so ket qua...")
    plt.show()
    return True


def get_image_input_interactive():
    """Ham nhan lua chon nguon anh tu nguoi dung (ho tro moi anh)."""
    print("\n" + "="*65)
    print("        CHUONG TRINH XU LY ANH TONG HOP (NOP BAI)")
    print("="*65)
    print("Hay chon cach dua anh vao (HO TRO MOI FILE ANH):")
    print("   [1] Nhan Enter (hoac go 1): Mo hop thoai de chon anh bat ky tu may tinh")
    print("   [2] Keo tha hoac nhap duong dan bat ky file anh nao vao day")
    print("   [3] Dan link anh internet (http:// hoac https://)")
    print("-"*65)

    while True:
        user_choice = input("👉 Nhap lua chon hoac duong dan anh: ").strip()

        # Nhan Enter hoac go 1 -> Mo hop thoai chon file
        if user_choice == "" or user_choice == "1":
            print("\n[*] Dang mo hop thoai chon file anh...")
            selected_path = select_image_file()
            if selected_path:
                return selected_path
            else:
                print("[!] Chua chon file tu hop thoai.")
                fallback = find_any_existing_image()
                if fallback:
                    print(f"[i] Su dung file anh co san: {fallback}")
                    return fallback
                continue

        cleaned_path = user_choice.strip('"').strip("'")

        if cleaned_path.startswith("http://") or cleaned_path.startswith("https://"):
            return cleaned_path

        if os.path.exists(cleaned_path):
            return cleaned_path
        else:
            print(f"[!] Khong tim thay file tai: '{cleaned_path}'. Vui long thu lai!")


def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = get_image_input_interactive()

    if image_path:
        process_and_display_all(image_path)


if __name__ == "__main__":
    main()
