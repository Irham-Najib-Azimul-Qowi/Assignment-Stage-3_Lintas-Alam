# Assignment-Stage-3_Lintas-Alam
Repositori ini dibuat untuk memenuhi assignment dari stage 3 sic batch 6 oleh tim Lintas Alam dengan kode tim UNI107

# Tutorial Setup: Sistem Absensi Wajah dengan ESP32 & Streamlit

Panduan ini menjelaskan cara mengatur dan menjalankan Sistem Absensi Wajah menggunakan ESP32-CAM, ESP32, Server Python, dan Streamlit.

---

## 📋 Prasyarat

**Perangkat Keras:**

*   ESP32-CAM (AI Thinker atau sejenisnya)
*   ESP32 Dev Board
*   Motor Servo SG90 (atau sejenisnya)
*   Layar OLED SSD1306 (I2C - 128x64)
*   Kabel Jumper
*   Power Supply (untuk ESP dan servo)
*   Komputer untuk menjalankan Server & Streamlit Client

**Perangkat Lunak:**

*   Python 3.x
*   Pip (Python package installer)
*   Arduino IDE
*   Thonny IDE (atau IDE MicroPython lain)
*   Firmware MicroPython untuk ESP32
*   MQTT Broker yang dapat diakses (contoh: `broker.emqx.io` publik atau broker lokal/pribadi)
*   (Opsional) Akun Ubidots untuk logging data

---

## 🔧 Konfigurasi Awal

Sebelum memulai, sesuaikan file-file berikut dengan pengaturan Anda:

1.  **Kredensial WiFi:**
    *   Buka `esp32cam.ino` (Arduino IDE): Ubah `YOUR_WIFI_SSID` dan `YOUR_WIFI_PASSWORD`.
    *   Buka `esp32_control.py` (Thonny IDE): Ubah `YOUR_WIFI_SSID` dan `YOUR_WIFI_PASSWORD`.

2.  **Token Ubidots (Opsional):**
    *   Buka `server.py`: Ubah `YOUR_UBIDOTS_TOKEN` dengan token Anda. Sesuaikan `UBIDOTS_DEVICE` jika nama device Ubidots Anda berbeda.

3.  **MQTT Broker:**
    *   Secara default, semua skrip (`server.py`, `app.py`, `esp32cam.ino`, `esp32_control.py`) menggunakan `broker.emqx.io:1883`. Jika Anda menggunakan broker lain, ganti alamat dan port di semua file tersebut.

4.  **Pin GPIO:**
    *   `esp32cam.ino`: Pin kamera standar untuk AI Thinker. Flash LED di pin `4`.
    *   `esp32_control.py`: Servo di pin `23`, OLED SDA di `21`, OLED SCL di `22`. Sesuaikan jika rangkaian Anda berbeda.

---

## ⚙️ Instalasi & Setup Komponen

Ikuti langkah-langkah ini untuk setiap komponen sistem:

### 1. Server (Komputer/VPS)

1.  **Siapkan Lingkungan Python:**
    ```bash
    # Buat environment virtual (disarankan)
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows

    # Instal dependensi
    pip install streamlit paho-mqtt opencv-python face_recognition numpy pandas requests
    ```
2.  **Buat Struktur Folder:**
    ```bash
    mkdir dataset encoding metadata
    ```
3.  **Siapkan Dataset Wajah Awal:**
    *   Buat subfolder di dalam `dataset` untuk setiap orang yang ingin didaftarkan.
    *   Masukkan beberapa file gambar (`.jpg` atau `.png`) wajah orang tersebut ke dalam subfolder masing-masing.
    *   Contoh struktur:
        ```
        dataset/
        ├── Budi/
        │   ├── foto1.jpg
        │   └── foto2.png
        └── Ani/
            └── foto_ani.jpg
        ```

### 2. ESP32-CAM (Arduino IDE)

1.  **Setup Arduino IDE:**
    *   Instal dukungan Board ESP32: Buka `File > Preferences`, tambahkan URL Board Manager: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`. Buka `Tools > Board > Boards Manager`, cari `esp32` dan instal.
    *   Pilih Board: `Tools > Board > ESP32 Arduino > AI Thinker ESP32-CAM` (atau yang sesuai).
2.  **Instal Library Arduino:**
    *   Buka `Tools > Manage Libraries...` dan instal:
        *   `PubSubClient` (oleh Nick O'Leary)
        *   `ESPAsyncWebServer`
        *   `AsyncTCP` (diperlukan oleh `ESPAsyncWebServer`)
3.  **Buka & Konfigurasi Kode:**
    *   Buka file `esp32cam.ino`.
    *   Pastikan Anda sudah mengatur **SSID & Password WiFi** (lihat bagian Konfigurasi Awal).
4.  **Upload Kode:**
    *   Hubungkan ESP32-CAM ke komputer (gunakan programmer FTDI jika perlu).
    *   Pastikan port yang benar dipilih di `Tools > Port`.
    *   Klik tombol Upload.
5.  **Verifikasi:**
    *   Buka `Tools > Serial Monitor` (atur baud rate ke `115200`).
    *   Anda akan melihat log koneksi WiFi dan alamat IP yang didapat. Catat alamat IP ini jika diperlukan untuk debugging.

### 3. ESP32 Kontrol (Thonny IDE & MicroPython)

1.  **Flash Firmware MicroPython:**
    *   Pastikan ESP32 Dev Board Anda sudah ter-flash dengan firmware MicroPython terbaru. Ikuti [dokumentasi resmi MicroPython](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) jika belum.
2.  **Setup Thonny IDE:**
    *   Buka Thonny IDE.
    *   Hubungkan ke ESP32 Anda: `Run > Select interpreter...`, pilih `MicroPython (ESP32)` dan port yang sesuai.
3.  **Instal Library MicroPython:**
    *   Di Thonny, buka `Tools > Manage packages...`.
    *   Cari dan instal:
        *   `micropython-umqtt.simple`
        *   `micropython-ssd1306`
    *   Jika tidak ditemukan, unduh manual file `.py` (misalnya `umqtt/simple.py` dan `ssd1306.py`) dan unggah ke ESP32 menggunakan Thonny (`File > Save copy...` lalu pilih `MicroPython device`).
4.  **Buka & Konfigurasi Kode:**
    *   Buka file `esp32_control.py`.
    *   Pastikan Anda sudah mengatur **SSID & Password WiFi** (lihat bagian Konfigurasi Awal).
5.  **Jalankan Kode:**
    *   Simpan file ke ESP32 sebagai `main.py` agar berjalan otomatis saat boot.
    *   Atau, jalankan langsung dari Thonny dengan menekan tombol Run (F5).
6.  **Verifikasi:**
    *   Layar OLED seharusnya menampilkan "System Ready".
    *   Periksa output di Shell/REPL Thonny untuk melihat status koneksi WiFi dan MQTT.

---

## ▶️ Menjalankan Sistem (Lokal)

Setelah semua komponen dikonfigurasi dan di-setup:

1.  **Nyalakan Perangkat ESP:**
    *   Pastikan ESP32-CAM dan ESP32 Kontrol menyala dan terhubung ke WiFi serta MQTT Broker.

2.  **Jalankan Server Python:**
    *   Buka terminal atau command prompt di komputer Anda.
    *   Arahkan ke direktori proyek.
    *   Aktifkan virtual environment (jika Anda menggunakannya): `source venv/bin/activate` atau `venv\Scripts\activate`.
    *   Jalankan server:
        ```bash
        python server.py
        ```
    *   Server akan mulai mendengarkan pesan MQTT (termasuk IP dari ESP32-CAM), memuat encoding wajah, dan mencoba memulai streaming video.

3.  **Jalankan Antarmuka Streamlit:**
    *   Buka terminal atau command prompt **baru**.
    *   Arahkan ke direktori proyek.
    *   Aktifkan virtual environment (jika perlu).
    *   Jalankan aplikasi Streamlit:
        ```bash
        streamlit run app.py
        ```
    *   Streamlit akan memberikan URL (biasanya `http://localhost:8501`). Buka URL ini di browser Anda.

4.  **Gunakan Aplikasi:**
    *   **Tab Settings:** Kelola dataset wajah (tambah/hapus orang). Server akan otomatis mendeteksi perubahan dan memperbarui encoding.
    *   **Tab Jadwal:** Atur jadwal absensi (umum atau perorangan).
    *   **Pengujian:** Arahkan wajah yang terdaftar ke ESP32-CAM.
    *   **Tab Presensi:** Jika wajah dikenali dan sesuai dengan jadwal, entri absensi akan muncul di sini.
    *   **Tab Log:** Lihat log aktivitas sistem dari server dan client.
    *   **Tab Ubidots:** Lihat dashboard Ubidots (jika dikonfigurasi).
    *   Perhatikan juga reaksi pada ESP32 Kontrol (servo bergerak, OLED menampilkan nama/status).

---

## ☁️ Catatan Deployment (Opsional)

Jika Anda ingin menjalankan ini secara online (misalnya Streamlit di Streamlit Cloud):

1.  **Server:** Jalankan `server.py` pada mesin yang dapat diakses publik (VPS, cloud instance) dan memiliki akses ke folder `dataset`, `encoding`, `metadata`.
2.  **Streamlit:** Deploy `app.py` dan `requirements.txt` (hanya berisi `streamlit`, `paho-mqtt`, `pandas`) ke platform hosting Streamlit (seperti Streamlit Cloud).
3.  **Konektivitas:** Pastikan *semua* komponen (Server, Streamlit Client, ESP32-CAM, ESP32 Kontrol) dapat terhubung ke **MQTT Broker yang sama**.
4.  **Sinkronisasi Dataset:** Mengelola dataset melalui Streamlit yang di-deploy memerlukan mekanisme sinkronisasi file antara instance Streamlit dan Server, atau API khusus. Perintah MQTT `update_dataset` hanya memberi tahu server untuk memuat ulang, file fisik harus ada di server.

---

Selamat mencoba!
