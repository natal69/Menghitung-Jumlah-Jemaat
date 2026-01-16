import cv2
import numpy as np
from ultralytics import YOLO
import cvzone

# --- 1. KONFIGURASI SISTEM ---
print("Menyiapkan Sistem...")
model = YOLO('yolov8n.pt')

# ==============================================================================
# [BAGIAN GANTI SUMBER KAMERA]
# Pilih salah satu (Webcam atau CCTV). Matikan yang tidak dipakai dengan tanda pagar '#'.
# ==============================================================================

# --- OPSI A: PAKAI WEBCAM LAPTOP (Untuk Testing Sekarang) ---
cap = cv2.VideoCapture(0)
# cap.set(3, 1280) # Lebar (Wajib diset manual kalau webcam laptop)
# cap.set(4, 720)  # Tinggi

# --- OPSI B: PAKAI CCTV ASLI (Nanti) ---
# Cara pakai: Hapus tanda pagar (#) pada 3 baris di bawah ini, dan beri pagar pada OPSI A.

# Format RTSP: "rtsp://username:password@IP_Address:Port/path"
# Contoh untuk Hikvision/Dahua biasanya seperti ini:
# rtsp_url = "rtsp://admin:password123@192.168.1.64:554/Streaming/Channels/101"
# cap = cv2.VideoCapture(rtsp_url)

# Catatan: CCTV biasanya otomatis mengirim resolusi aslinya, jadi cap.set(3,...) seringkali tidak perlu.

# ==============================================================================

# --- 2. KONFIGURASI GARIS BATAS (SENSOR VIRTUAL) ---
# Sesuaikan 'posisi_garis' ini nanti saat di lokasi asli
# Jika resolusi CCTV beda (misal 1920x1080), angkanya harus disesuaikan lagi.
posisi_garis = 200

# Garis Horizontal [x1, y1, x2, y2]
# Angka 1280 sesuaikan dengan lebar resolusi kamera nanti
limits = [100, posisi_garis, 1180, posisi_garis]

# Variabel Penyimpan Data
totalMasuk = []   
totalKeluar = []  
track_history = {} 

print("Sistem Siap! Menghadap ke Luar Pintu (45 Derajat)")

while True:
    success, frame = cap.read()
    if not success:
        # Jika CCTV putus koneksi, loop akan berhenti atau bisa dibuat reconnect logic
        print("Gagal membaca frame kamera (Cek koneksi CCTV/Webcam)")
        break

    # Jika pakai CCTV resolusi tinggi (misal 4K), resize dulu biar laptop ga berat
    # frame = cv2.resize(frame, (1280, 720)) 

    # --- 3. DETEKSI & TRACKING ---
    results = model.track(frame, persist=True, conf=0.5, classes=[0], verbose=False)

    # Gambar Garis Merah
    cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 4)
    cvzone.putTextRect(frame, "GARIS PINTU", (limits[0], limits[1]-10), scale=1, thickness=1, colorR=(0,0,255))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            
            if box.id is not None:
                id = int(box.id[0])
                cx, cy = x1 + w // 2, y1 + h // 2
                
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # --- 4. LOGIKA ARAH GERAK ---
                if id not in track_history:
                    track_history[id] = []
                
                track_history[id].append(cy)
                
                if len(track_history[id]) > 2:
                    prev_y = track_history[id][-2]
                    curr_y = track_history[id][-1]
                    
                    if limits[1] - 20 < cy < limits[1] + 20:
                        # MASUK (Atas ke Bawah)
                        if totalMasuk.count(id) == 0: 
                            if curr_y > prev_y: 
                                totalMasuk.append(id)
                                cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

                        # KELUAR (Bawah ke Atas)
                        if totalKeluar.count(id) == 0: 
                            if curr_y < prev_y: 
                                totalKeluar.append(id)
                                cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 255), 5)

                cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(frame, f'ID: {id}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # --- 5. TAMPILAN DASHBOARD ---
    di_dalam = len(totalMasuk) - len(totalKeluar)
    if di_dalam < 0: di_dalam = 0

    cvzone.putTextRect(frame, f'MASUK: {len(totalMasuk)}', (50, 50), scale=2, thickness=2, colorR=(0, 200, 0))
    cvzone.putTextRect(frame, f'KELUAR: {len(totalKeluar)}', (50, 110), scale=2, thickness=2, colorR=(0, 0, 200))
    cvzone.putTextRect(frame, f'DI DALAM: {di_dalam}', (50, 170), scale=2, thickness=2, colorR=(50, 50, 50))

    cv2.imshow("Sistem CCTV Gereja (45 Derajat)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()