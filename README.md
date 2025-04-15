# 📘 Sistem Absensi Wajah dengan ESP32 & Streamlit

Panduan ini menjelaskan cara setup dan menjalankan sistem absensi wajah menggunakan ESP32-CAM, ESP32, server Python, dan antarmuka pengguna berbasis Streamlit.

---

## 📦 Perangkat yang Dibutuhkan

### Perangkat Keras:
- ESP32-CAM (AI Thinker)
- ESP32 Dev Board
- Motor Servo SG90
- Layar OLED SSD1306 (I2C - 128x64)
- Kabel Jumper
- Power Supply (untuk ESP dan servo)
- Komputer (untuk menjalankan server dan Streamlit)

### Perangkat Lunak:
- Python 3.x
- Arduino IDE
- Thonny IDE (MicroPython)
- MQTT Broker (contoh: broker.emqx.io)

---

## ⚙️ Instalasi & Setup

### 1. Konfigurasi ESP32-CAM (Arduino IDE):
- Tambahkan board URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
- Board: AI Thinker ESP32-CAM
- Library:
  - PubSubClient
  - ESPAsyncWebServer
  - AsyncTCP
- File: `esp32cam.ino`
  - Ubah SSID & Password WiFi
  - Upload ke board dan buka Serial Monitor (baud 115200)

### 2. Konfigurasi ESP32 (Thonny IDE & MicroPython):
- Flash firmware MicroPython
- Jalankan `esp32_control.py`
  - Gunakan pin: Servo (GPIO 23), OLED SDA (21), SCL (22)
  - Library:
    - umqtt.simple
    - ssd1306
- OLED akan menampilkan status koneksi dan nama yang dikenali

### 3. Server Python:
- Buat virtual environment dan install:
```bash
pip install streamlit paho-mqtt opencv-python face_recognition numpy pandas requests
```
- Struktur folder:
```
dataset/
├── Budi/
│   ├── 1.jpg
└── Ani/
    └── 1.jpg
```
- Jalankan `server.py` untuk menerima data MQTT dan memproses pengenalan wajah.

### 4. Streamlit UI:
- Jalankan dengan:
```bash
streamlit run app.py
```
- Fungsi:
  - Tambah data wajah
  - Lihat log absensi
  - Jadwal absensi
  - Tampilkan status dari ESP32

---

## 📡 MQTT Default
Gunakan `broker.emqx.io` port 1883. Jika ingin mengganti, ubah di semua file:
- `server.py`
- `app.py`
- `esp32cam.ino`
- `esp32_control.py`

---

## 🚀 Menjalankan Sistem
1. Nyalakan ESP32-CAM dan ESP32.
2. Jalankan `server.py` di komputer.
3. Jalankan `app.py` dengan Streamlit.
4. Buka `http://localhost:8501` untuk UI absensi.

---

## 📤 Deployment (Opsional)
- Jalankan `server.py` di VPS/cloud.
- Deploy `app.py` ke Streamlit Cloud.
- Pastikan semua koneksi ke broker MQTT dapat dilakukan dari perangkat.

---

## 📝 Catatan
- Dataset wajah minimal 1 foto per orang.
- Sinkronisasi dataset dilakukan manual atau menggunakan API.

Selamat mencoba!

