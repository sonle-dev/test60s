# HE THONG XU LY ANH TONG HOP (NOP BAI)

## 1. Tinh nang noi bat
- **Ho tro moi loai anh**: Nhan bat ky file anh nao (.jpg, .png, .jpeg, .bmp, .webp, .tiff...) voi moi do phan giai, moi ten file (ke ca ten tieng Viet co dau, co khoang trang).
- **Tu dong thich ung kich thuoc**: Anh thu 2 duoc tao tu dong theo dung chieu dai va chieu rong cua anh dau vao, dam bao phep cong/tru anh khong bao gio bi loi sai kich thuoc.
- **Khong bi rang buoc ten anh**: Giao dien hien thi tong quat, khong bi dinh ten co dinh, khong lo loi ky tu.

## 2. 12 Khung hien thi tong hop de nop bai:
1. Anh Goc Input (hien thi do phan giai thuc te)
2. Histogram 3 Mau (RGB)
3. Tang Do Tuong Phan (alpha=1.6)
4. Giam Do Tuong Phan (alpha=0.5)
5. Can Bang Histogram (khong gian YCrCb - kenh Y)
6. Histogram Sau Can Bang
7. Tach Nguong Otsu (tu dong tinh nguong toi uu)
8. Anh Am Ban (Negative)
9. Anh Thu 2 (mau tu dong tao dong kich thuoc)
10. Cong Anh (cv2.add bao hoa 255)
11. Tru Anh (cv2.absdiff tri tuyet doi)
12. Bang Thong So Ky Thuat Xu Ly

## 3. Cai dat thu vien tren may moi:
Neu mang sang may tinh moi (chua co thu vien), ban mo Terminal/CMD len va chay 1 lenh duy nhat:
```powershell
pip install -r requirements.txt
```
Hoac cai dat truc tiep:
```powershell
pip install opencv-python matplotlib numpy pillow
```

## 4. Cach chay chuong trinh:
```powershell
python main.py
```
- Nhan **Enter** de mo hop thoai chon bat ky file anh nao tu may tinh.
- Hoac keo tha file anh truc tiep vao Terminal.
- Ket qua xuat tu dong ra: `ket_qua_nop_bai.png`.
