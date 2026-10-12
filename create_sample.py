"""
Script tạo ảnh mẫu phong phú màu sắc để kiểm tra bài thực hành Histogram
"""
import sys
import numpy as np
import cv2

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_sample_image(output_path="sample.jpg"):
    # Tạo ảnh kích thước 400x600 có các vùng màu sắc đa dạng và gradient
    height, width = 400, 600
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # 1. Nền gradient đa sắc
    for y in range(height):
        for x in range(width):
            img[y, x, 0] = int(255 * (x / width))        # Kênh B (OpenCV BGR)
            img[y, x, 1] = int(255 * (y / height))       # Kênh G
            img[y, x, 2] = int(255 * ((x + y) / (width + height))) # Kênh R

    # 2. Vẽ các hình khối màu rõ rệt
    # Vùng Đỏ (Red trong BGR là (0, 0, 255))
    cv2.circle(img, (150, 150), 90, (0, 0, 255), -1)
    # Vùng Xanh lá (Green trong BGR là (0, 255, 0))
    cv2.circle(img, (300, 250), 90, (0, 255, 0), -1)
    # Vùng Xanh dương (Blue trong BGR là (255, 0, 0))
    cv2.circle(img, (450, 150), 90, (255, 0, 0), -1)
    # Vùng Vàng (Yellow = Red + Green trong BGR là (0, 255, 255))
    cv2.rectangle(img, (220, 50), (380, 130), (0, 255, 255), -1)

    cv2.imwrite(output_path, img)
    print(f"Da tao anh mau thanh cong tai: {output_path}")

if __name__ == "__main__":
    generate_sample_image()
