from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
import utime
import network
import umqtt.simple

# Konfigurasi WiFi
WIFI_SSID = "ssid"  # Ganti dengan SSID WiFi Anda
WIFI_PASSWORD = "password"  # Ganti dengan kata sandi WiFi Anda

# Konfigurasi MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_door"
MQTT_TOPIC_DOOR = "lintas_alam/door"
MQTT_TOPIC_OLED = "lintas_alam/oled"

# Konfigurasi Servo
SERVO_PIN = 23
servo = PWM(Pin(SERVO_PIN), freq=50)  # Frekuensi 50Hz

# Konfigurasi OLED
I2C_SDA = 21
I2C_SCL = 22
i2c = I2C(1, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Konfigurasi sudut servo
# - CLOSE_ANGLE: Sudut saat pintu tertutup (default: 0°)
# - OPEN_ANGLE: Sudut saat pintu terbuka (default: 90°, ke kiri relatif terhadap 0°)
# Jika arah terbalik, tukar nilai (misalnya, CLOSE_ANGLE = 90, OPEN_ANGLE = 0)
CLOSE_ANGLE = 0
OPEN_ANGLE = 90

# Fungsi untuk mengatur sudut servo
def set_servo_angle(angle):
    angle = max(0, min(180, angle))  # Batasi sudut antara 0° dan 180°
    pulse_width = 500 + (1900 * angle // 180)  # 500us (0°) hingga 2400us (180°)
    duty = int(pulse_width * 1023 // 20000)  # Skala ke duty cycle
    servo.duty(duty)
    print("Servo set to:", angle, "degrees")

# Fungsi untuk menampilkan teks di OLED
def display_text(text):
    oled.fill(0)
    lines = text.split('\n')
    y = 0
    for line in lines:
        if y < OLED_HEIGHT - 8:
            oled.text(line[:16], 0, y)  # Maks 16 karakter per baris
            y += 8
    oled.show()
    print("OLED displaying:", text)

# Fungsi untuk menghubungkan WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 10
        start = utime.time()
        while not wlan.isconnected():
            if utime.time() - start > timeout:
                print("WiFi connection timeout")
                return False
            utime.sleep_ms(500)
    print("WiFi connected:", wlan.ifconfig())
    return True

# Callback MQTT saat pesan diterima
def on_message(topic, msg):
    topic_str = topic.decode()
    message = msg.decode()
    print(f"Received on {topic_str}: {message}")
    if topic_str == MQTT_TOPIC_DOOR:
        if message == "OPEN":
            set_servo_angle(OPEN_ANGLE)  # Pintu terbuka (ke kiri)
        elif message == "CLOSE":
            set_servo_angle(CLOSE_ANGLE)  # Pintu tertutup
    elif topic_str == MQTT_TOPIC_OLED:
        display_text(message)

# Inisialisasi MQTT
def init_mqtt():
    try:
        client = umqtt.simple.MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.set_callback(on_message)
        client.connect()
        client.subscribe(MQTT_TOPIC_DOOR)
        client.subscribe(MQTT_TOPIC_OLED)
        print("Connected to MQTT broker")
        return client
    except Exception as e:
        print("MQTT connection failed:", e)
        return None

# Main program
def main():
    # Hubungkan WiFi
    if not connect_wifi():
        display_text("WiFi Failed")
        while True:
            utime.sleep(1)

    # Inisialisasi OLED
    display_text("Initializing...")
    utime.sleep_ms(2000)

    # Inisialisasi Servo
    set_servo_angle(CLOSE_ANGLE)  # Pintu tertutup saat start
    display_text("Absen Ditutup!\nSilahkan Hubungi Dosen!")

    # Inisialisasi MQTT
    client = init_mqtt()
    if client is None:
        display_text("MQTT Failed")
        while True:
            utime.sleep(1)

    # Loop utama
    while True:
        try:
            client.check_msg()  # Periksa pesan MQTT
            utime.sleep_ms(100)
        except Exception as e:
            print("MQTT error:", e)
            client.disconnect()
            client = init_mqtt()
            if client is None:
                display_text("MQTT Failed")
                utime.sleep(5)
                display_text("Absen Ditutup!\nSilahkan Hubungi Dosen!")

if __name__ == "__main__":
    main()
