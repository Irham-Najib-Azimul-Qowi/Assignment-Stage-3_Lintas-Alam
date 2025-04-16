Proyek Absensi Otomatis Lintas Alam (Kode Tim: UNI107)
Selamat datang di repositori Assignment-Stage-3_Lintas-Alam! Proyek ini adalah solusi absensi otomatis berbasis teknologi IoT dan pengenalan wajah, dikembangkan oleh Tim Lintas Alam (Kode Tim: UNI107). Sistem ini mengintegrasikan ESP32-CAM untuk streaming video, ESP32 dengan layar OLED dan servo untuk kontrol pintu, aplikasi Streamlit untuk manajemen jadwal dan kontrol manual, serta penyimpanan data absensi di Ubidots dan file CSV. Proyek ini dirancang untuk lingkungan akademik, memungkinkan absensi otomatis dengan verifikasi wajah.
Deskripsi Proyek
Proyek ini bertujuan menciptakan sistem absensi otomatis yang efisien dengan fitur-fitur berikut:

Pengenalan Wajah: Menggunakan ESP32-CAM untuk streaming video dan library face_recognition di server Python untuk mendeteksi dan mengenali wajah.
Kontrol Pintu Otomatis: Servo MG90S membuka dan menutup pintu berdasarkan hasil pengenalan wajah.
Tampilan Status: Layar OLED SSD1306 (128x64, I2C) pada ESP32 menampilkan status absensi, seperti "Silahkan Absen!" atau nama mahasiswa yang absen.
Manajemen Jadwal: Aplikasi Streamlit memungkinkan pengaturan jadwal absensi untuk mata kuliah atau individu, dengan kontrol manual untuk flash, pintu, dan pesan OLED.
Integrasi IoT: Semua perangkat berkomunikasi melalui protokol MQTT menggunakan broker publik broker.emqx.io.
Penyimpanan Data: Data absensi dikirim ke platform Ubidots untuk visualisasi dan disimpan lokal dalam file CSV (attendance_log.csv).

Struktur Repositori
Berikut adalah daftar file dalam repositori beserta fungsinya:

esp32cam.ino: Kode Arduino untuk ESP32-CAM, menangani streaming video MJPEG, kontrol flash (GPIO4), dan komunikasi MQTT untuk menerima perintah flash dan mengirim IP perangkat.
camera_pins.h: File header yang mendefinisikan konfigurasi pin untuk berbagai model kamera ESP32-CAM (default: AI-Thinker).
esp32.py: Kode MicroPython untuk ESP32 Dev Module, mengontrol servo MG90S (GPIO23), layar OLED SSD1306 (I2C, GPIO21 dan GPIO22), dan komunikasi MQTT untuk menerima perintah pintu dan pesan OLED.
ssd1306.py: Driver MicroPython untuk layar OLED SSD1306, mendukung antarmuka I2C dan SPI.
server.py: Script Python untuk server, menangani pengenalan wajah menggunakan face_recognition, komunikasi MQTT, pengiriman data absensi ke Ubidots, dan penyimpanan log absensi dalam CSV.
streamlit.py: Aplikasi Streamlit untuk antarmuka pengguna, memungkinkan pengaturan jadwal absensi, kontrol flash/pintu/OLED, dan melihat log aktivitas MQTT.
requirements.txt: Daftar dependensi Python minimal untuk streamlit.py (termasuk streamlit dan paho-mqtt).

Komponen Hardware
Berikut adalah daftar lengkap komponen hardware yang diperlukan:

ESP32-CAM (dengan modul kamera OV2640): Untuk streaming video dan pengenalan wajah. Pastikan model AI-Thinker untuk kompatibilitas dengan camera_pins.h.
ESP32 Dev Module (misalnya, ESP32-WROOM-32): Untuk mengontrol servo dan layar OLED. Modul dengan 30/38 pin disarankan untuk kemudahan koneksi.
Servo MG90S: Motor servo untuk membuka/tutup pintu (sudut 0°-90°). Memerlukan daya 5V stabil.
Layar OLED SSD1306 (128x64, I2C): Menampilkan status absensi. Menggunakan protokol I2C untuk komunikasi.
FTDI USB-to-Serial Adapter atau ESP32 Downloader: Untuk mengunggah kode ke ESP32-CAM, yang tidak memiliki port USB bawaan.
Kabel USB:
Tipe-A ke Micro-USB untuk ESP32-CAM (via FTDI).
Tipe-A ke USB-C untuk ESP32 Dev Module (tergantung model).


Jumper Wires (Male-to-Female dan Male-to-Male): Untuk menghubungkan servo, OLED, dan komponen lain. Minimal 10 kabel.
Breadboard (400 lubang atau lebih): Untuk perakitan rangkaian sementara.
PCB (opsional): Untuk rangkaian permanen menggunakan soldering.
Power Supply (opsional): Adaptor 5V/2A dengan konektor Micro-USB/USB-C untuk daya eksternal jika USB tidak cukup.
Komputer: Untuk menjalankan server.py, streamlit.py, dan mengunggah kode ke ESP32-CAM/ESP32. Spesifikasi minimal: Windows 10/11, macOS, atau Linux dengan RAM 4GB.
Router WiFi: Untuk koneksi internet ESP32-CAM dan ESP32 ke broker MQTT. Pastikan sinyal stabil.

Catatan Hardware

ESP32-CAM memerlukan daya 5V stabil. Jika menggunakan FTDI, pastikan FTDI mendukung arus hingga 500mA.
Servo MG90S dapat menarik arus tinggi (hingga 700mA saat berputar). Gunakan sumber daya eksternal jika ESP32 tidak cukup kuat.
OLED SSD1306 harus mendukung I2C (alamat default: 0x3C). Periksa dokumentasi jika alamat berbeda.

Prasyarat Software
Pastikan kamu memiliki perangkat lunak berikut sebelum memulai:

Arduino IDE (versi 2.x atau terbaru): Untuk mengunggah kode ke ESP32-CAM.
Thonny IDE (versi 4.x atau terbaru): Untuk mengunggah kode MicroPython ke ESP32.
Python 3.8+: Untuk menjalankan server.py dan streamlit.py. Python 3.9 direkomendasikan untuk kompatibilitas maksimal.
Git: Untuk mengelola repositori (opsional, jika ingin clone atau push).
Akun Streamlit Cloud: Untuk deploy aplikasi Streamlit (daftar gratis di streamlit.io/cloud).
Akun Ubidots: Untuk menyimpan dan memvisualisasikan data absensi (daftar gratis di ubidots.com).
Koneksi WiFi Stabil: Dengan SSID dan kata sandi untuk ESP32-CAM dan ESP32.

Dependensi Python
Berikut adalah daftar lengkap dependensi Python untuk menjalankan server.py dan streamlit.py. Instalasi dilakukan melalui pip.
Untuk streamlit.py
Dependensi minimal ada di requirements.txt:
pip install streamlit==1.29.0 paho-mqtt==2.1.0

Untuk server.py
Dependensi tambahan diperlukan untuk pengenalan wajah, pemrosesan gambar, dan komunikasi:
pip install paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11

Catatan Instalasi face_recognition

Library face_recognition memerlukan dlib, yang bisa sulit diinstal di beberapa sistem. Pastikan kamu memiliki:

CMake dan kompiler C++ (misalnya, Visual Studio Build Tools di Windows).
Python 3.7-3.9 (versi 3.10+ mungkin bermasalah).


Jika instalasi dlib gagal, coba:
pip install dlib --verbose

Atau, instal precompiled wheel dari sumber tidak resmi seperti PyPI atau:
pip install dlib-bin


Di Windows, instal Visual Studio Community dengan workload "Desktop development with C++".

Di Linux, instal dependensi:
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev


Di macOS, instal dependensi:
brew install cmake libpng



Instalasi Semua Dependensi Sekaligus
Jalankan perintah berikut untuk menginstal semua dependensi:
pip install streamlit==1.29.0 paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11

Tutorial Penggunaan
Berikut adalah panduan langkah demi langkah untuk menyiapkan dan menjalankan semua komponen proyek.
1. Menyiapkan ESP32-CAM di Arduino IDE
ESP32-CAM bertanggung jawab untuk streaming video MJPEG dan kontrol flash (lampu LED pada GPIO4).
Langkah-langkah:

Instal Arduino IDE:

Unduh dari arduino.cc (versi 2.x direkomendasikan).
Instal dan buka Arduino IDE.


Tambahkan Board ESP32:

Buka File > Preferences.

Di Additional Boards Manager URLs, tambahkan:
https://raw.githubusercontent.com/espressif/arduino-esp32/master/package_esp32_index.json


Buka Tools > Board > Boards Manager, cari esp32, dan instal ESP32 by Espressif Systems (versi terbaru).



Instal Library:

Buka Sketch > Include Library > Manage Libraries.
Cari dan instal:
ESP32 (sudah termasuk esp_camera.h)
WiFi (bawaan ESP32)
WebServer (bawaan ESP32)
PubSubClient (oleh Nick O'Leary, versi 2.x)


Jika library tidak ditemukan, unduh PubSubClient dari GitHub dan tambahkan via Sketch > Include Library > Add .ZIP Library.


Hubungkan ESP32-CAM:

Gunakan FTDI USB-to-Serial Adapter atau ESP32 Downloader untuk menghubungkan ESP32-CAM ke komputer.
Koneksi FTDI:
VCC (FTDI) → 5V (ESP32-CAM)
GND (FTDI) → GND (ESP32-CAM)
TX (FTDI) → RX (U0R, GPIO3)
RX (FTDI) → TX (U0T, GPIO1)
Jumper GPIO0 ke GND saat upload kode (gunakan jumper wire).


Pastikan driver FTDI terinstal:
Windows: Unduh dari ftdichip.com.
macOS/Linux: Biasanya otomatis terdeteksi.


Setelah upload, lepaskan jumper GPIO0 untuk menjalankan kode.


Konfigurasi Kode:

Buka file esp32cam.ino di Arduino IDE.

Edit konfigurasi WiFi:
const char* ssid = "ssid"; // Ganti dengan SSID WiFi kamu
const char* password = "password"; // Ganti dengan kata sandi WiFi


Pastikan model kamera sesuai di baris:
#define CAMERA_MODEL_AI_THINKER


Jika menggunakan model lain (misalnya, WROVER_KIT), ubah sesuai opsi di camera_pins.h.




Upload Kode:

Pilih board: Tools > Board > ESP32 Arduino > ESP32-CAM.

Pilih port: Tools > Port (misalnya, COM3 di Windows atau /dev/ttyUSB0 di Linux).

Tekan tombol Boot di ESP32-CAM, lalu klik Upload di Arduino IDE.

Jika upload gagal:

Pastikan jumper GPIO0 terhubung ke GND.
Cek driver FTDI/port COM.
Gunakan kabel USB berkualitas.


Setelah upload selesai, buka Serial Monitor (baud rate: 115200) untuk melihat IP ESP32-CAM, misalnya:
Streaming tersedia di: http://192.168.1.100/stream




Uji Coba:

Buka browser, masukkan URL streaming dari Serial Monitor (misalnya, http://192.168.1.100/stream).
Kamu akan melihat streaming video MJPEG dari ESP32-CAM.
Uji kontrol flash dengan mengirim pesan MQTT via Streamlit (lihat bagian Streamlit):
Topic: lintas_alam/lampu1
Pesan: ON atau OFF.





Troubleshooting ESP32-CAM:

Port Tidak Terdeteksi:
Instal driver FTDI atau CP2102 (tergantung adapter).
Cek Device Manager (Windows) atau ls /dev/tty* (Linux/macOS).


Upload Gagal:
Pastikan jumper GPIO0 ke GND saat upload.
Tekan tombol Boot sebelum klik Upload.
Coba port USB lain atau komputer lain.


Streaming Tidak Muncul:
Pastikan ESP32-CAM terhubung ke WiFi (cek SSID/password).
Cek firewall; pastikan port 80 tidak diblokir.
Uji dengan http://<IP>/capture untuk gambar statis.



2. Menyiapkan ESP32 di Thonny (MicroPython)
ESP32 Dev Module mengontrol servo MG90S untuk pintu dan layar OLED SSD1306 untuk status absensi.
Langkah-langkah:

Instal Thonny:

Unduh dari thonny.org (versi 4.x direkomendasikan).
Instal dan buka Thonny.


Instal MicroPython di ESP32:

Unduh firmware MicroPython untuk ESP32 dari micropython.org.

Pilih firmware stabil (misalnya, esp32-20230426-v1.20.0.bin).

Hubungkan ESP32 ke komputer via kabel USB.

Instal esptool untuk flashing:
pip install esptool


Hapus flash dan unggah firmware:
esptool.py --port COMX erase_flash
esptool.py --port COMX write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

Ganti COMX dengan port ESP32 (misalnya, COM4) dan nama file firmware sesuai yang diunduh.

Jika port tidak terdeteksi, instal driver CP2102 dari silabs.com.



Konfigurasi Thonny:

Buka Tools > Options > Interpreter.
Pilih MicroPython (ESP32) sebagai interpreter.
Pilih port COM yang sesuai (misalnya, COM4).
Klik Install or update MicroPython jika ingin instal firmware via Thonny.


Unggah File:

Buka file esp32.py dan ssd1306.py di Thonny.

Edit esp32.py untuk konfigurasi WiFi:
WIFI_SSID = "ssid"  # Ganti dengan SSID WiFi kamu
WIFI_PASSWORD = "password"  # Ganti dengan kata sandi WiFi


Klik kanan pada esp32.py dan ssd1306.py, pilih Upload to / untuk mengunggah ke ESP32.

Simpan esp32.py sebagai main.py di ESP32:

Klik kanan esp32.py, pilih Upload to /main.py.
Ini memastikan kode berjalan otomatis saat ESP32 dinyalakan.




Hubungkan Hardware:

Servo MG90S:

VCC (merah) → 5V (ESP32, pin VIN jika pakai USB)
GND (cokelat) → GND (ESP32)
Signal (oranye) → GPIO23


OLED SSD1306 (I2C):

VCC → 3.3V (ESP32)
GND → GND (ESP32)
SDA → GPIO21
SCL → GPIO22


Gunakan breadboard untuk koneksi. Pastikan kabel jumper kuat dan tidak longgar.

Diagram koneksi (contoh):
ESP32       Servo MG90S       OLED SSD1306
VIN  ----> VCC (merah)      
GND  ----> GND (cokelat) ----> GND
GPIO23 --> Signal (oranye)
3.3V  ---------------------> VCC
GPIO21 --------------------> SDA
GPIO22 --------------------> SCL




Uji Coba:

Nyalakan ESP32 (hubungkan ke USB atau power supply).

OLED akan menampilkan:
Initializing...

Lalu, jika tidak ada jadwal aktif:
Absen Ditutup!
Silahkan Hubungi Dosen!


Uji servo dengan mengirim pesan MQTT via Streamlit:

Topic: lintas_alam/door
Pesan: OPEN (servo berputar ke OPEN_ANGLE, default 90°) atau CLOSE (ke CLOSE_ANGLE, default 0°).


Uji OLED dengan mengirim pesan MQTT:

Topic: lintas_alam/oled
Pesan: Misalnya, Tes OLED.





Troubleshooting ESP32:

ESP32 Tidak Terdeteksi:

Instal driver CP2102 atau CH340 (tergantung modul ESP32).
Cek port di Device Manager (Windows) atau ls /dev/tty* (Linux/macOS).


OLED Tidak Menampilkan:

Cek koneksi I2C (SDA, SCL). Gunakan multimeter untuk memastikan kontinuitas.

Jalankan kode I2C scanner untuk memeriksa alamat OLED:
from machine import Pin, I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21))
print(i2c.scan())

Alamat default OLED adalah 0x3C. Jika berbeda, ubah di esp32.py.



Servo Tidak Bergerak:

Cek daya (servo memerlukan arus tinggi). Gunakan power supply 5V eksternal jika perlu.

Pastikan sudut di esp32.py sesuai (OPEN_ANGLE, CLOSE_ANGLE). Jika terbalik, tukar nilai (misalnya, OPEN_ANGLE=0, CLOSE_ANGLE=90).

Uji servo dengan kode sederhana:
from machine import Pin, PWM
servo = PWM(Pin(23), freq=50)
servo.duty(77)  # Sudut ~90°





3. Menjalankan Server (server.py)
Server menangani pengenalan wajah, komunikasi MQTT, pengiriman data ke Ubidots, dan penyimpanan log absensi.
Langkah-langkah:

Instal Python:

Unduh Python 3.8 atau 3.9 dari python.org. Hindari Python 3.10+ karena masalah kompatibilitas face_recognition.

Pastikan pip terinstal:
python -m ensurepip --upgrade
python -m pip install --upgrade pip




Instal Dependensi:

Buka terminal di folder proyek.

Instal semua dependensi:
pip install paho-mqtt==2.1.0 opencv-python==4.8.1.78 numpy==1.24.3 face_recognition==1.3.0 requests==2.31.0 pandas==2.0.3 pickle5==0.0.11


Jika face_recognition gagal, instal dependensi dlib terlebih dahulu (lihat catatan di atas).



Siapkan Dataset Wajah:

Buat folder dataset di direktori yang sama dengan server.py.

Untuk setiap orang, buat subfolder dengan nama (misalnya, dataset/John_Doe).

Tambahkan minimal 3-5 gambar wajah per orang (format .jpg atau .png, resolusi minimal 640x480).

Contoh struktur:
dataset/
├── John_Doe/
│   ├── image1.jpg
│   ├── image2.jpg
│   ├── image3.jpg
├── Jane_Smith/
│   ├── image1.jpg
│   ├── image2.jpg


Pastikan wajah jelas, dengan pencahayaan baik dan sudut beragam untuk akurasi pengenalan.



Konfigurasi Ubidots:

Daftar di ubidots.com (akun gratis untuk pendidikan).

Buat perangkat baru di dashboard Ubidots (nama: face_recognation).

Dapatkan UBIDOTS_TOKEN dari API Credentials di profil Ubidots.

Edit server.py:
UBIDOTS_TOKEN = "BBUS-w4hoDRHaDcWGfZAO4RZITgVz6EoLhq"  # Ganti dengan token kamu




Jalankan Server:

Pastikan ESP32-CAM menyala dan terhubung ke WiFi (IP dikirim via MQTT ke topic lintas_alam/ip).

Jalankan server.py:
python server.py


Server akan:

Memuat dataset wajah dari folder dataset.
Terhubung ke MQTT broker (broker.emqx.io).
Mulai streaming video dari ESP32-CAM (menggunakan IP dari MQTT).
Menampilkan jendela OpenCV dengan kotak dan nama wajah yang dikenali.
Mencetak tabel absensi di terminal setiap 30 frame.
Menyimpan log absensi ke attendance_log.csv.
Mengirim data absensi ke Ubidots.




Uji Coba:

Hadapkan wajah ke ESP32-CAM.
Jika wajah dikenali dan sesuai jadwal (dari Streamlit):
Jendela OpenCV menunjukkan kotak hijau dengan nama.
Pintu terbuka (servo bergerak, dikontrol via MQTT lintas_alam/door).
OLED menampilkan pesan seperti John_Doe telah absen.
Data absensi muncul di dashboard Ubidots.


Cek attendance_log.csv untuk log lokal.
Tekan q di jendela OpenCV untuk menghentikan server.



Troubleshooting Server:

Streaming Video Gagal:
Pastikan IP ESP32-CAM benar (cek log server atau MQTT topic lintas_alam/ip).
Uji streaming di browser (http://<IP>/stream).
Cek firewall; pastikan port 80 terbuka.


Pengenalan Wajah Tidak Akurat:
Tambahkan lebih banyak gambar ke dataset (minimal 5 per orang).
Pastikan pencahayaan baik dan wajah tidak buram.
Sesuaikan tolerance di server.py (default: 0.5). Nilai lebih kecil (misalnya, 0.4) untuk akurasi lebih ketat.


Ubidots Tidak Menerima Data:
Cek token di server.py.
Pastikan koneksi internet stabil.
Buka dashboard Ubidots, cek variabel person_presence dan attendance_timestamp.


Jendela OpenCV Tidak Muncul:
Pastikan opencv-python terinstal.
Cek apakah frame diterima (tambahkan print("Frame received") di get_mjpeg_frame).



4. Deploy Streamlit ke Streamlit Cloud
Aplikasi Streamlit (streamlit.py) menyediakan antarmuka untuk mengatur jadwal absensi, mengontrol flash/pintu/OLED, dan melihat log MQTT.
Langkah-langkah:

Instal Streamlit Lokal:

Instal dependensi:
pip install streamlit==1.29.0 paho-mqtt==2.1.0


Uji lokal:
streamlit run streamlit.py


Buka http://localhost:8501 di browser untuk melihat aplikasi.



Siapkan Repositori GitHub:

Pastikan file streamlit.py dan requirements.txt ada di repositori.

Commit dan push:
git add streamlit.py requirements.txt
git commit -m "Menambahkan aplikasi Streamlit"
git push origin main


Jika folder streamlit-absensi masih ada di GitHub, hapus via web (lihat percakapan sebelumnya):

Buka github.com/Irham-Najib-Azimul-Qowi/Assignment-Stage-3_Lintas-Alam.
Navigasi ke streamlit-absensi, hapus setiap file dengan ikon sampah.
Commit hingga folder kosong dan hilang.




Buat Akun Streamlit Cloud:

Daftar di streamlit.io/cloud menggunakan akun GitHub.
Login dan buat aplikasi baru.


Deploy ke Streamlit Cloud:

Di dashboard Streamlit Cloud, klik New app.
Pilih repositori Irham-Najib-Azimul-Qowi/Assignment-Stage-3_Lintas-Alam.
Pilih branch main dan file utama streamlit.py.
Klik Advanced settings:
Set Python version ke 3.9.
Tambahkan secrets jika diperlukan (opsional untuk MQTT publik).


Klik Deploy.
Tunggu 2-5 menit hingga aplikasi aktif di URL seperti https://your-app-name.streamlit.app.


Uji Coba:

Buka URL aplikasi Streamlit.
Uji fitur:
Tab Jadwal:
Masukkan nama mata kuliah, tanggal, dan waktu untuk jadwal absensi.
Atur jadwal perorangan dengan nama dan waktu.
Klik Simpan Jadwal untuk mengirim ke MQTT (lintas_alam/schedule).


Tab Kontrol:
Klik Flash ON/OFF untuk mengontrol lampu ESP32-CAM (lintas_alam/lampu1).
Klik Buka/Tutup Pintu untuk mengontrol servo (lintas_alam/door).
Masukkan pesan dan klik Kirim Pesan ke OLED (lintas_alam/oled).


Tab Log:
Lihat log aktivitas MQTT (koneksi, publikasi, error).




Pastikan aplikasi terhubung ke broker.emqx.io (cek log jika gagal).



Troubleshooting Streamlit:

MQTT Tidak Terhubung:

Cek koneksi internet.

Pastikan broker broker.emqx.io aktif (uji dengan client MQTT lain, seperti MQTT Explorer).

Tambahkan log tambahan di streamlit.py:
logger.debug("Mencoba terhubung ke MQTT...")




Aplikasi Tidak Deploy:

Cek requirements.txt (pastikan versi spesifik, misalnya, streamlit==1.29.0).
Periksa log deploy di Streamlit Cloud untuk error (misalnya, Python version salah).
Pastikan file streamlit.py ada di root repositori.


Tombol Tidak Berfungsi:

Cek log di tab Log untuk pesan error.
Pastikan MQTT client aktif (st.session_state.mqtt_client).



5. Menjalankan Seluruh Sistem

Nyalakan ESP32-CAM:

Pastikan esp32cam.ino terunggah.
Hubungkan ke WiFi dan catat IP dari Serial Monitor.
Uji streaming di browser (http://<IP>/stream).


Nyalakan ESP32:

Pastikan esp32.py dan ssd1306.py terunggah sebagai main.py dan ssd1306.py.
OLED menampilkan status awal.
Servo berada di posisi tertutup (CLOSE_ANGLE).


Jalankan Server:

Jalankan server.py di komputer.
Pastikan dataset wajah tersedia di folder dataset.
Server akan terhubung ke MQTT dan mulai streaming.


Akses Streamlit:

Buka aplikasi Streamlit (lokal di http://localhost:8501 atau di Streamlit Cloud).
Atur jadwal absensi (mata kuliah atau perorangan).
Uji kontrol manual (flash, pintu, OLED).


Uji Absensi:

Hadapkan wajah ke ESP32-CAM.
Jika wajah dikenali dan sesuai jadwal:
Server mendeteksi wajah dan menampilkan nama di jendela OpenCV.
Mengirim perintah OPEN ke lintas_alam/door (servo bergerak).
Mengirim pesan ke lintas_alam/oled (misalnya, John_Doe telah absen).
Data absensi dikirim ke Ubidots dan disimpan di attendance_log.csv.


Setelah 7 detik, pintu ditutup (CLOSE).



Contoh Alur Absensi:

Mahasiswa John Doe mendekati ESP32-CAM pada jam 08:00.

Jadwal mata kuliah "Matematika" aktif (08:00-09:00, diatur via Streamlit).

Server mengenali wajah John Doe.

Servo membuka pintu, OLED menampilkan:
John_Doe telah absen
Silahkan masuk!


Data absensi (name: John_Doe, timestamp: 2025-04-16 08:00:00, status: Hadir, course: Matematika) dikirim ke Ubidots dan disimpan di CSV.

Setelah 7 detik, pintu menutup, dan OLED kembali ke status default.


Troubleshooting Lanjutan

ESP32-CAM Tidak Terhubung ke WiFi:

Cek SSID dan password di esp32cam.ino.

Pastikan router mendukung 2.4GHz (ESP32-CAM tidak mendukung 5GHz).

Tambahkan debug di setup():
Serial.println(WiFi.status());




Servo Bergetar:

Servo MG90S memerlukan daya stabil. Gunakan kapasitor 100uF antara VCC dan GND servo.
Cek kode PWM di esp32.py; pastikan freq=50.


OLED Menampilkan Karakter Acak:

Cek alamat I2C (default: 0x3C).
Pastikan kabel I2C tidak terlalu panjang (>30cm dapat menyebabkan noise).


Streamlit Lambat atau Crash:

Di Streamlit Cloud, tingkatkan resource (opsi berbayar) atau uji lokal.
Kurangi log berlebihan di streamlit.py untuk performa lebih baik.


Dataset Wajah Tidak Dimuat:

Cek path dataset di server.py.

Pastikan gambar tidak korup (buka dengan image viewer).

Tambahkan debug di load_known_faces():
print(f"Memuat gambar: {image_path}")




MQTT Broker Tidak Respons:

Uji koneksi ke broker.emqx.io dengan MQTT client (misalnya, MQTT Explorer).
Ganti broker jika perlu (misalnya, test.mosquitto.org).



Kontribusi
Ingin berkontribusi? Ikuti langkah berikut:

Fork repositori ini.
Buat branch baru (git checkout -b fitur-baru).
Commit perubahan (git commit -m "Menambahkan fitur X").
Push ke branch (git push origin fitur-baru).
Ajukan pull request di GitHub.

Pastikan kode terdokumentasi dan lulus tes lokal sebelum mengajukan PR.
Kontak
Untuk pertanyaan atau dukungan, hubungi Tim Lintas Alam (UNI107):

Email: jockytugas@gmail.com
GitHub Issues: Buka issue di repositori ini untuk bug atau pertanyaan teknis.


Dibuat oleh Tim Lintas Alam (Kode Tim: UNI107)Solusi Absensi Otomatis untuk Masa Depan AkademikTanggal Pembuatan: 16 April 2025
