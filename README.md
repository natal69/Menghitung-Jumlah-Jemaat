# 📷 Sistem Penghitung Jemaat Real-Time (YOLOv8)

Sistem penghitung otomatis berbasis Computer Vision untuk memantau jumlah jemaat yang masuk dan keluar gereja secara real-time. Sistem ini menggunakan **YOLOv8** untuk deteksi objek dan algoritma tracking untuk menghitung arah pergerakan.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![OpenCV](https://img.shields.io/badge/Library-OpenCV-red)

## 🌟 Fitur Utama
* **Deteksi Manusia Akurat:** Menggunakan YOLOv8 yang difilter khusus untuk mendeteksi manusia (Class 0).
* **Penghitung Dua Arah:** Menghitung jemaat **MASUK** dan **KELUAR**.
* **Real-Time Occupancy:** Menampilkan jumlah jemaat yang ada **DI DALAM** ruangan saat ini.
* **Dukungan CCTV & Webcam:** Bisa menggunakan webcam laptop atau IP Camera (RTSP).
* **Optimasi Sudut Pandang:** Dirancang khusus untuk kamera di atas pintu dengan sudut kemiringan **45 derajat** menghadap luar.

## 🛠️ Teknologi yang Digunakan
* **Python 3.11** (Bahasa Pemrograman)
* **Ultralytics YOLOv8** (Deteksi Objek AI)
* **OpenCV** (Pengolahan Citra Video)
* **Cvzone** (Visualisasi Tampilan)

## 🚀 Cara Instalasi

1.  **Clone Repository ini**
    ```bash
    git clone [https://github.com/username-kamu/nama-repo-kamu.git](https://github.com/username-kamu/nama-repo-kamu.git)
    cd nama-repo-kamu
    ```

2.  **Install Library yang Dibutuhkan**
    Pastikan Python sudah terinstall, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Program**
    ```bash
    python main.py
    ```
    *Saat pertama kali dijalankan, sistem akan otomatis mendownload model `yolov8n.pt`.*

## ⚙️ Konfigurasi & Penggunaan

### 1. Mengatur Sumber Kamera (Webcam / CCTV)
Buka file `main.py`, cari bagian **SWITCH CCTV**:
* **Webcam Laptop:** Gunakan `cap = cv2.VideoCapture(0)`
* **CCTV (RTSP):** Uncomment baris RTSP dan isi sesuai IP kamera kamu.
    ```python
    # Contoh format RTSP
    cap = cv2.VideoCapture("rtsp://admin:password@192.168.1.10:554/stream1")
    ```

### 2. Kalibrasi Garis Hitung
Ubah variabel `posisi_garis` di `main.py` agar garis merah pas berada di lantai ambang pintu.
```python
posisi_garis = 450  # Sesuaikan angka ini (0 - 720)
