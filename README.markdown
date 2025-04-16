# 🌟 Proyek Absensi Otomatis Lintas Alam (Kode Tim: UNI107)

Selamat datang di repositori **Assignment-Stage-3_Lintas-Alam**! 🚀 Proyek ini adalah solusi absensi otomatis berbasis IoT dan pengenalan wajah, dikembangkan oleh **Tim Lintas Alam** (Kode Tim: UNI107). Sistem ini mengintegrasikan **ESP32-CAM** untuk streaming video, **ESP32** dengan layar OLED dan servo untuk kontrol pintu, serta aplikasi **Streamlit** untuk manajemen jadwal dan kontrol manual. Data absensi disimpan di **Ubidots** ☁️ dan file CSV 📊 untuk lingkungan akademik yang lebih efisien.

---

## 📝 Deskripsi Proyek

Proyek ini dirancang untuk menciptakan sistem absensi otomatis yang cerdas dengan fitur berikut:

- **👤 Pengenalan Wajah**: Menggunakan ESP32-CAM untuk streaming video dan library `face_recognition` di server Python untuk mendeteksi serta mengenali wajah.
- **🚪 Kontrol Pintu Otomatis**: Servo MG90S membuka/tutup pintu berdasarkan hasil pengenalan wajah.
- **🖥️ Tampilan Status**: Layar OLED SSD1306 (128x64, I2C) menampilkan status seperti "Silahkan Absen!" atau nama mahasiswa.
- **📅 Manajemen Jadwal**: Aplikasi Streamlit memungkinkan pengaturan jadwal absensi mata kuliah atau perorangan, plus kontrol manual untuk flash, pintu, dan OLED.
- **🌐 Integrasi IoT**: Komunikasi antar perangkat melalui protokol MQTT dengan broker publik `broker.emqx.io`.
- **💾 Penyimpanan Data**: Data absensi dikirim ke Ubidots untuk visualisasi dan disimpan lokal di `attendance_log.csv`.

---

## 📂 Struktur Repositori

Berikut daftar file beserta fungsinya:

| File | Fungsi |
| --- | --- |
| `esp32cam.ino` | Kode Arduino untuk ESP32-CAM: streaming video MJPEG, kontrol flash (GPIO4), dan MQTT. |
| `camera_pins.h` | Konfigurasi pin untuk model kamera ESP32-CAM (default: AI-Thinker). |
| `esp32.py` | Kode MicroPython untuk ESP32: kontrol servo MG90S (GPIO23), OLED SSD1306 (I2C, GPIO21 & GPIO22), dan MQTT. |
| `ssd1306.py` | Driver MicroPython untuk layar OLED SSD1306 (I2C/SPI). |
| `server.py` | Script Python untuk pengenalan wajah, komunikasi MQTT, data ke Ubidots, dan log CSV. |
| `streamlit.py` | Aplikasi Streamlit untuk jadwal absensi, kontrol flash/pintu/OLED, dan log MQTT. |
| `requirements.txt` | Daftar dependensi Python untuk `streamlit.py` (`streamlit`, `paho-mqtt`). |

---

## 🔧 Komponen Hardware

Berikut komponen yang diperlukan untuk menjalankan proyek:

| Komponen | Deskripsi |
| --- | --- |
| **ESP32-CAM (OV2640)** | Streaming video dan pengenalan wajah. Gunakan model AI-Thinker. |
| **ESP32 Dev Module** | Kontrol servo dan OLED. Rekomendasi: ESP32-WROOM-32 (30/38 pin). |
| **Servo MG90S** | Membuka/tutup pintu (sudut 0°-90°). Membutuhkan daya 5V stabil. |
| **Layar OLED SSD1306** | Tampilan status absensi (128x64, I2C, alamat default: 0x3C). |
| **FTDI/ESP32 Downloader** | Mengunggah kode ke ESP32-CAM (tanpa port USB bawaan). |
| **Kabel USB** | Tipe-A ke Micro-USB (ESP32-CAM via FTDI), Tipe-A ke USB-C (ESP32). |
| **Jumper Wires** | Male-to-Female/Male-to-Male untuk koneksi servo, OLED, dll. (min. 10). |
| **Breadboard** | Perakitan rangkaian sementara (min. 400 lubang). |
| **PCB (opsional)** | Untuk rangkaian permanen dengan soldering. |
| **Power Supply (opsional)** | Adaptor 5V/2A untuk daya eksternal jika USB tidak cukup. |
| **Komputer** | Jalankan `server.py`, `streamlit.py`, dan unggah kode. Min: 4GB RAM. |
| **Router WiFi** | Koneksi internet untuk ESP32-CAM/ESP32 ke MQTT. Pastikan sinyal stabil. |

### ⚠️ Catatan Hardware

- **ESP32-CAM**: Membutuhkan daya 5V stabil. Pastikan FTDI mendukung arus hingga 500mA.
- **Servo MG90S**: Konsumsi arus hingga 700mA saat berputar. Gunakan daya eksternal jika perlu.
- **OLED SSD1306**: Harus mendukung I2C. Periksa alamat (default: 0x3C) di dokumentasi.

---

## 🛠️ Prasyarat Software

Pastikan kamu memiliki:

- **Arduino IDE** (v2.x+): Untuk mengunggah kode ke ESP32-CAM.
- **Thonny IDE** (v4.x+): Untuk kode MicroPython di ESP32.
- **Python 3.8+**: Untuk `server.py` dan `streamlit.py`. Python 3.9 direkomendasikan.
- **Git** (opsional): Untuk mengelola repositori.
- **Akun Streamlit Cloud**: Deploy aplikasi Streamlit (gratis di streamlit.io/cloud).
- **Akun Ubidots**: Simpan dan visualisasikan data absensi (gratis di ubidots.com).
- **WiFi Stabil**: SSID dan kata sandi untuk ESP32-CAM dan ESP32.

---

## 📦 Dependensi Python

Instal dependensi melalui `pip` untuk menjalankan `server.py` dan `streamlit.py`.

### Untuk `streamlit.py`

Daftar minimal di `requirements.txt`:

```bash
pip install streamlit==1.29.0 paho-mqtt==2.1.0
```

### Untuk `server.py`

Dependensi tambahan untuk pengenalan wajah dan komunikasi:

```bash
pip install paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11
```

### ⚠️ Catatan Instalasi `face_recognition`

Library `face_recognition` membutuhkan `dlib`, yang memerlukan:

- **CMake** dan kompiler C++ (contoh: Visual Studio Build Tools di Windows).
- **Python 3.7-3.9** (3.10+ mungkin bermasalah).

Jika `dlib` gagal:

```bash
pip install dlib --verbose
```

Atau gunakan precompiled wheel:

```bash
pip install dlib-bin
```

**Windows**:

- Instal Visual Studio Community dengan workload "Desktop development with C++".

**Linux**:

```bash
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
```

**macOS**:

```bash
brew install cmake libpng
```

### Instalasi Semua Dependensi

```bash
pip install streamlit==1.29.0 paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11
```

---

## 📚 Tutorial Penggunaan

Berikut panduan langkah demi langkah untuk menyiapkan dan menjalankan proyek.

### 1. 🎥 Menyiapkan ESP32-CAM di Arduino IDE

ESP32-CAM menangani streaming video MJPEG dan kontrol flash (LED pada GPIO4).

#### Langkah-langkah:

1. **Instal Arduino IDE**:

   - Unduh dari arduino.cc (v2.x+).
   - Buka Arduino IDE.

2. **Tambahkan Board ESP32**:

   - Buka **File &gt; Preferences**.

   - Tambahkan URL di **Additional Boards Manager URLs**:

     ```plaintext
     https://raw.githubusercontent.com/espressif/arduino-esp32/master/package_esp32_index.json
     ```

   - Buka **Tools &gt; Board &gt; Boards Manager**, cari `esp32`, instal **ESP32 by Espressif Systems**.

3. **Instal Library**:

   - Buka **Sketch &gt; Include Library &gt; Manage Libraries**.
   - Instal:
     - `ESP32` (termasuk `esp_camera.h`)
     - `WiFi`
     - `WebServer`
     - `PubSubClient` (Nick O'Leary, v2.x+)
   - Alternatif: Unduh `PubSubClient` dari GitHub, tambahkan via **Add .ZIP Library**.

4. **Hubungkan ESP32-CAM**:

   - Gunakan **FTDI USB-to-Serial Adapter** atau **ESP32 Downloader**.
   - Koneksi FTDI:
     - VCC (FTDI) → 5V (ESP32-CAM)
     - GND (FTDI) → GND (ESP32-CAM)
     - TX (FTDI) → RX (U0R, GPIO3)
     - RX (FTDI) → TX (U0T, GPIO1)
     - Jumper GPIO0 ke GND saat upload kode.
   - Instal driver FTDI dari ftdichip.com.
   - Lepaskan jumper GPIO0 setelah upload.

5. **Konfigurasi Kode**:

   - Buka `esp32cam.ino`.

   - Edit WiFi:

     ```cpp
     const char* ssid = "ssid"; // Ganti dengan SSID WiFi
     const char* password = "password"; // Ganti dengan kata sandi
     ```

   - Pastikan model kamera:

     ```cpp
     #define CAMERA_MODEL_AI_THINKER
     ```

     Sesuaikan dengan `camera_pins.h` jika model berbeda.

6. **Upload Kode**:

   - Pilih **Tools &gt; Board &gt; ESP32 Arduino &gt; ESP32-CAM**.

   - Pilih port di **Tools &gt; Port**.

   - Tekan tombol **Boot**, klik **Upload**.

   - Buka **Serial Monitor** (115200 baud) untuk melihat IP, misalnya:

     ```plaintext
     Streaming tersedia di: http://192.168.1.100/stream
     ```

7. **Uji Coba**:

   - Buka URL streaming di browser (contoh: `http://192.168.1.100/stream`).
   - Lihat video MJPEG.
   - Uji flash via Streamlit:
     - Topic: `lintas_alam/lampu1`
     - Pesan: `ON`/`OFF`.

#### 🔍 Troubleshooting

- **Port Tidak Terdeteksi**: Instal driver FTDI/CP2102. Cek Device Manager (Windows) atau `ls /dev/tty*` (Linux/macOS).
- **Upload Gagal**: Pastikan jumper GPIO0 ke GND. Tekan **Boot** sebelum upload.
- **Streaming Gagal**: Cek SSID/password. Pastikan port 80 tidak diblokir firewall.

---

### 2. ⚙️ Menyiapkan ESP32 di Thonny (MicroPython)

ESP32 mengontrol servo MG90S (pintu) dan OLED SSD1306 (status).

#### Langkah-langkah:

1. **Instal Thonny**:

   - Unduh dari thonny.org (v4.x+).
   - Buka Thonny.

2. **Instal MicroPython**:

   - Unduh firmware dari micropython.org (contoh: `esp32-20230426-v1.20.0.bin`).

   - Hubungkan ESP32 via USB.

   - Instal `esptool`:

     ```bash
     pip install esptool
     ```

   - Flash firmware:

     ```bash
     esptool.py --port COMX erase_flash
     esptool.py --port COMX write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
     ```

     Ganti `COMX` dengan port ESP32.

3. **Konfigurasi Thonny**:

   - Buka **Tools &gt; Options &gt; Interpreter**.
   - Pilih **MicroPython (ESP32)** dan port COM.
   - Instal driver CP2102 dari silabs.com jika port tidak terdeteksi.

4. **Unggah File**:

   - Buka `esp32.py` dan `ssd1306.py`.

   - Edit WiFi di `esp32.py`:

     ```python
     WIFI_SSID = "ssid"  # Ganti SSID
     WIFI_PASSWORD = "password"  # Ganti kata sandi
     ```

   - Klik kanan file, pilih **Upload to /**.

   - Simpan `esp32.py` sebagai `main.py` untuk autorun.

5. **Hubungkan Hardware**:

   - **Servo MG90S**:
     - VCC (merah) → 5V (ESP32, VIN)
     - GND (cokelat) → GND
     - Signal (oranye) → GPIO23
   - **OLED SSD1306 (I2C)**:
     - VCC → 3.3V
     - GND → GND
     - SDA → GPIO21
     - SCL → GPIO22

   **Diagram Koneksi**:

   ```
   ESP32       Servo MG90S       OLED SSD1306
   VIN  ----> VCC (merah)      
   GND  ----> GND (cokelat) ----> GND
   GPIO23 --> Signal (oranye)
   3.3V  ---------------------> VCC
   GPIO21 --------------------> SDA
   GPIO22 --------------------> SCL
   ```

6. **Uji Coba**:

   - Nyalakan ESP32. OLED menampilkan:

     ```
     Initializing...
     Absen Ditutup!
     Silahkan Hubungi Dosen!
     ```

   - Uji servo via Streamlit:

     - Topic: `lintas_alam/door`
     - Pesan: `OPEN`/`CLOSE`

   - Uji OLED:

     - Topic: `lintas_alam/oled`
     - Pesan: `Tes OLED`.

#### 🔍 Troubleshooting

- **ESP32 Tidak Terdeteksi**: Instal driver CP2102/CH340.

- **OLED Tidak Menampilkan**:

  - Cek koneksi I2C. Jalankan I2C scanner:

    ```python
    from machine import Pin, I2C
    i2c = I2C(1, scl=Pin(22), sda=Pin(21))
    print(i2c.scan())
    ```

  - Sesuaikan alamat (default: 0x3C) di `esp32.py`.

- **Servo Tidak Bergerak**:

  - Cek daya (gunakan power supply 5V jika perlu).

  - Uji dengan:

    ```python
    from machine import Pin, PWM
    servo = PWM(Pin(23), freq=50)
    servo.duty(77)  # ~90°
    ```

---

### 3. 🖥️ Menjalankan Server (`server.py`)

Server menangani pengenalan wajah, MQTT, Ubidots, dan log CSV.

#### Langkah-langkah:

1. **Instal Python**:

   - Unduh Python 3.8/3.9 dari python.org.

   - Pastikan `pip`:

     ```bash
     python -m ensurepip --upgrade
     python -m pip install --upgrade pip
     ```

2. **Instal Dependensi**:

   ```bash
   pip install paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11
   ```

3. **Siapkan Dataset Wajah**:

   - Buat folder `dataset` di direktori `server.py`.

   - Tambahkan subfolder per orang (contoh: `dataset/John_Doe`).

   - Masukkan 3-5 gambar wajah per orang (.jpg/.png, min. 640x480).

     ```
     dataset/
     ├── John_Doe/
     │   ├── image1.jpg
     │   ├── image2.jpg
     ├── Jane_Smith/
     │   ├── image1.jpg
     ```

4. **Konfigurasi Ubidots**:

   - Daftar di ubidots.com (gratis).

   - Buat perangkat `face_recognation`.

   - Ambil **UBIDOTS_TOKEN** dari **API Credentials**.

   - Edit `server.py`:

     ```python
     UBIDOTS_TOKEN = "your-token-here"
     ```

5. **Jalankan Server**:

   ```bash
   python server.py
   ```

   - Server akan:
     - Memuat dataset wajah.
     - Terhubung ke `broker.emqx.io`.
     - Streaming video dari ESP32-CAM (via IP di `lintas_alam/ip`).
     - Tampilkan wajah di jendela OpenCV.
     - Log absensi ke `attendance_log.csv` dan Ubidots.

6. **Uji Coba**:

   - Hadapkan wajah ke ESP32-CAM.
   - Jika sesuai jadwal:
     - OpenCV menampilkan kotak hijau dan nama.
     - Pintu terbuka (`lintas_alam/door`, `OPEN`).
     - OLED menampilkan pesan (contoh: `John_Doe telah absen`).
     - Data ke Ubidots dan CSV.
   - Tekan `q` untuk menghentikan.

#### 🔍 Troubleshooting

- **Streaming Gagal**: Cek IP ESP32-CAM di log atau `lintas_alam/ip`. Uji di browser (`http://<IP>/stream`).

- **Pengenalan Wajah Buruk**: Tambah gambar dataset. Sesuaikan `tolerance` di `server.py` (misalnya, 0.4).

- **Ubidots Gagal**: Verifikasi token. Cek variabel `person_presence` di dashboard.

- **OpenCV Error**: Tambahkan debug:

  ```python
  print("Frame received")
  ```

---

### 4. ☁️ Deploy Streamlit ke Streamlit Cloud

Streamlit mengatur jadwal dan kontrol manual.

#### Langkah-langkah:

1. **Instal Streamlit Lokal**:

   ```bash
   pip install streamlit==1.29.0 paho-mqtt==2.1.0
   streamlit run streamlit.py
   ```

   - Buka `http://localhost:8501`.

2. **Siapkan Repositori**:

   - Pastikan `streamlit.py` dan `requirements.txt` di root.

   - Commit:

     ```bash
     git add streamlit.py requirements.txt
     git commit -m "Tambah Streamlit"
     git push origin main
     ```

3. **Akun Streamlit Cloud**:

   - Daftar di streamlit.io/cloud via GitHub.

4. **Deploy**:

   - Klik **New app** di dashboard.
   - Pilih repositori `Irham-Najib-Azimul-Qowi/Assignment-Stage-3_Lintas-Alam`.
   - Set branch `main`, file `streamlit.py`.
   - **Advanced settings**: Python 3.9.
   - Klik **Deploy**. Tunggu hingga aktif (contoh: `https://your-app.streamlit.app`).

5. **Uji Coba**:

   - Buka URL Streamlit.
   - **Tab Jadwal**: Atur mata kuliah/individu, simpan ke `lintas_alam/schedule`.
   - **Tab Kontrol**:
     - Flash: `lintas_alam/lampu1` (`ON`/`OFF`).
     - Pintu: `lintas_alam/door` (`OPEN`/`CLOSE`).
     - OLED: `lintas_alam/oled` (kirim pesan).
   - **Tab Log**: Lihat aktivitas MQTT.

#### 🔍 Troubleshooting

- **MQTT Gagal**: Cek `broker.emqx.io` dengan MQTT Explorer.
- **Deploy Gagal**: Periksa log di Streamlit Cloud. Pastikan `requirements.txt` benar.
- **Tombol Error**: Cek log di tab **Log**.

---

### 5. 🚀 Menjalankan Seluruh Sistem

1. **ESP32-CAM**:

   - Unggah `esp32cam.ino`.
   - Catat IP dari Serial Monitor.
   - Uji streaming (`http://<IP>/stream`).

2. **ESP32**:

   - Unggah `esp32.py` sebagai `main.py`, `ssd1306.py`.
   - OLED menampilkan status. Servo tertutup.

3. **Server**:

   - Jalankan `server.py`.
   - Pastikan dataset wajah ada.

4. **Streamlit**:

   - Buka lokal atau di Streamlit Cloud.
   - Atur jadwal. Uji kontrol.

5. **Uji Absensi**:

   - Hadapkan wajah ke ESP32-CAM.
   - Jika sesuai jadwal:
     - Pintu terbuka.
     - OLED menampilkan nama.
     - Data ke Ubidots/CSV.
   - Pintu menutup setelah 7 detik.

#### 📋 Contoh Alur

- **08:00**: John Doe dekati ESP32-CAM.
- **Jadwal**: Matematika (08:00-09:00).
- **Hasil**:
  - Wajah dikenali.
  - Pintu terbuka, OLED: `John_Doe telah absen`.
  - Data: `name: John_Doe, timestamp: 2025-04-16 08:00:00, status: Hadir, course: Matematika`.
  - Pintu menutup setelah 7 detik.

---

## 🛠️ Troubleshooting Lanjutan

| Masalah | Solusi |
| --- | --- |
| **ESP32-CAM Tidak ke WiFi** | Cek SSID/password. Gunakan 2.4GHz. Debug: `Serial.println(WiFi.status());` |
| **Servo Bergetar** | Tambah kapasitor 100uF di VCC/GND. Pastikan `freq=50` di `esp32.py`. |
| **OLED Karakter Acak** | Cek I2C (max 30cm kabel). Verifikasi alamat (0x3C). |
| **Streamlit Lambat** | Uji lokal. Kurangi log di `streamlit.py`. |
| **Dataset Gagal Dimuat** | Cek path. Pastikan gambar valid. Debug: `print(f"Memuat: {image_path}")`. |
| **MQTT Tidak Respons** | Uji `broker.emqx.io` dengan MQTT Explorer. Coba `test.mosquitto.org`. |

---

## 🤝 Kontribusi

Ingin membantu? 😊

1. Fork repositori.
2. Buat branch (`git checkout -b fitur-baru`).
3. Commit (`git commit -m "Fitur X"`).
4. Push (`git push origin fitur-baru`).
5. Ajukan pull request.

Pastikan kode terdokumentasi dan dites lokal.

---

## 📬 Kontak

Hubungi **Tim Lintas Alam (UNI107)**:

- **Email**: jockytugas@gmail.com
- **GitHub Issues**: Buka issue di repositori untuk bug atau pertanyaan.

---

**Dibuat oleh Tim Lintas Alam (UNI107)**\
*Solusi Absensi Otomatis untuk Masa Depan Akademik*\
📅 *16 April 2025*