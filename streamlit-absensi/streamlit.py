import time
import streamlit as st
import json
import paho.mqtt.client as mqtt
from datetime import datetime
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfigurasi MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC_FLASH = "lintas_alam/lampu"
MQTT_TOPIC_SCHEDULE = "lintas_alam/schedule"
MQTT_TOPIC_DOOR = "lintas_alam/door"
MQTT_TOPIC_OLED = "lintas_alam/oled"

# Inisialisasi Session State
def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.mqtt_client = None
        st.session_state.mqtt_connected = False
        st.session_state.log_messages = []
        logger.info("Session state initialized")

initialize_session_state()

# MQTT Callback & Inisialisasi
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        st.session_state.mqtt_connected = True
        msg = "Terhubung ke MQTT Broker"
        st.session_state.log_messages.append(msg)
        logger.info(msg)
    else:
        st.session_state.mqtt_connected = False
        msg = f"Gagal terhubung ke MQTT Broker, kode: {rc}"
        st.session_state.log_messages.append(msg)
        logger.error(msg)

def on_disconnect(client, userdata, rc, properties=None):
    st.session_state.mqtt_connected = False
    msg = f"Terputus dari MQTT Broker, rc={rc}"
    st.session_state.log_messages.append(msg)
    logger.warning(msg)

def init_mqtt():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        return client
    except Exception as e:
        msg = f"Gagal menghubungkan ke MQTT Broker: {e}"
        st.session_state.log_messages.append(msg)
        logger.error(msg)
        return None

# Fungsi untuk menjalankan loop MQTT
def mqtt_loop(client):
    try:
        client.loop_forever()
    except Exception as e:
        msg = f"Error dalam MQTT loop: {e}"
        st.session_state.log_messages.append(msg)
        logger.error(msg)
        while True:
            try:
                client.reconnect()
                msg = "Berhasil reconnect ke MQTT Broker"
                st.session_state.log_messages.append(msg)
                logger.info(msg)
                break
            except Exception as e:
                msg = f"Gagal reconnect ke MQTT: {e}"
                st.session_state.log_messages.append(msg)
                logger.error(msg)
                time.sleep(5)

# Inisialisasi MQTT client
if st.session_state.mqtt_client is None:
    st.session_state.mqtt_client = init_mqtt()
    if st.session_state.mqtt_client is not None:
        mqtt_thread = threading.Thread(target=mqtt_loop, args=(st.session_state.mqtt_client,), daemon=True)
        mqtt_thread.start()
        st.session_state.log_messages.append("MQTT client initialized and loop started")
        logger.info("MQTT client initialized and loop started")
    else:
        st.session_state.log_messages.append("Failed to initialize MQTT client")
        logger.error("Failed to initialize MQTT client")

# Fungsi untuk mengirim perintah MQTT
def publish_command(topic, message):
    if st.session_state.mqtt_client is not None:
        if not st.session_state.mqtt_connected:
            msg = "MQTT client tidak terhubung, mencoba reconnect..."
            st.session_state.log_messages.append(msg)
            logger.warning(msg)
            try:
                st.session_state.mqtt_client.reconnect()
            except Exception as e:
                msg = f"Gagal reconnect ke MQTT: {e}"
                st.session_state.log_messages.append(msg)
                logger.error(msg)
                return
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = st.session_state.mqtt_client.publish(topic, message)
                if result.rc == 0:
                    msg = f"Publikasi ke {topic} berhasil: {message}"
                    st.session_state.log_messages.append(msg)
                    logger.info(msg)
                    break
                else:
                    msg = f"Publikasi ke {topic} gagal, rc={result.rc}"
                    st.session_state.log_messages.append(msg)
                    logger.error(msg)
            except Exception as e:
                msg = f"Percobaan {attempt + 1} gagal: {e}"
                st.session_state.log_messages.append(msg)
                logger.error(msg)
                time.sleep(1)
    else:
        msg = "MQTT client tidak tersedia"
        st.session_state.log_messages.append(msg)
        logger.error(msg)

# Fungsi untuk mengirim jadwal mata kuliah
def publish_course_schedule(course_name, start_datetime, end_datetime):
    payload = {
        "course": course_name,
        "start": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "end": end_datetime.strftime("%Y-%m-%d %H:%M:%S")
    }
    publish_command(MQTT_TOPIC_SCHEDULE, json.dumps(payload))

# Fungsi untuk mengirim jadwal perorangan
def publish_individual_schedule(person, start_datetime, end_datetime):
    payload = {
        "person": person,
        "start": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "end": end_datetime.strftime("%Y-%m-%d %H:%M:%S")
    }
    publish_command(MQTT_TOPIC_SCHEDULE, json.dumps(payload))

# Tampilan Utama
st.title("Aplikasi Kontrol Absensi")
st.write("Aplikasi ini digunakan untuk mengirim perintah ke sistem absensi melalui MQTT.")
tabs = st.tabs(["Jadwal", "Kontrol", "Log"])

# TAB 1: Jadwal
with tabs[0]:
    st.header("Jadwal")
    st.subheader("Atur Jadwal Absen Mata Kuliah")
    course_name = st.text_input("Nama Mata Kuliah", key="course_name")
    schedule_date = st.date_input("Tanggal Absen", value=datetime.now().date(), key="schedule_date")
    start_time_course = st.time_input("Waktu Mulai", value=datetime.strptime("06:00", "%H:%M").time(), key="start_time_course")
    end_time_course = st.time_input("Waktu Selesai", value=datetime.strptime("07:00", "%H:%M").time(), key="end_time_course")

    if st.button("Simpan Jadwal Absen Mata Kuliah"):
        start_datetime = datetime.combine(schedule_date, start_time_course)
        end_datetime = datetime.combine(schedule_date, end_time_course)
        if end_datetime > start_datetime:
            publish_course_schedule(course_name, start_datetime, end_datetime)
            st.success(f"Jadwal absen untuk {course_name} disimpan: {start_datetime} - {end_datetime}")
        else:
            st.error("Waktu selesai harus lebih besar dari waktu mulai!")

    st.subheader("Atur Jadwal Absen Perorangan")
    person_name = st.text_input("Nama Orang", key="person_name")
    schedule_date_individual = st.date_input("Tanggal Absen", value=datetime.now().date(), key="schedule_date_individual")
    start_time_individual = st.time_input("Waktu Mulai", value=datetime.strptime("06:00", "%H:%M").time(), key="start_time_individual")
    end_time_individual = st.time_input("Waktu Selesai", value=datetime.strptime("07:00", "%H:%M").time(), key="end_time_individual")

    if st.button("Simpan Jadwal Absen Perorangan"):
        start_datetime = datetime.combine(schedule_date_individual, start_time_individual)
        end_datetime = datetime.combine(schedule_date_individual, end_time_individual)
        if end_datetime > start_datetime:
            publish_individual_schedule(person_name, start_datetime, end_datetime)
            st.success(f"Jadwal untuk {person_name}: {start_datetime} - {end_datetime}")
        else:
            st.error("Waktu selesai harus lebih besar dari waktu mulai!")

# TAB 2: Kontrol
with tabs[1]:
    st.header("Kontrol")
    st.subheader("Kontrol Flash ESP32-CAM")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Flash ON"):
            publish_command(MQTT_TOPIC_FLASH, "ON")
    with col2:
        if st.button("Flash OFF"):
            publish_command(MQTT_TOPIC_FLASH, "OFF")

    st.subheader("Kontrol Pintu Manual")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Buka Pintu"):
            publish_command(MQTT_TOPIC_DOOR, "OPEN")
    with col4:
        if st.button("Tutup Pintu"):
            publish_command(MQTT_TOPIC_DOOR, "CLOSE")

    st.subheader("Kontrol OLED")
    oled_message = st.text_input("Pesan untuk OLED", key="oled_message")
    if st.button("Kirim Pesan ke OLED"):
        if oled_message:
            publish_command(MQTT_TOPIC_OLED, oled_message)
            st.success(f"Pesan '{oled_message}' dikirim ke OLED")
        else:
            st.error("Masukkan pesan terlebih dahulu!")

# TAB 3: Log
with tabs[2]:
    st.header("Log Aktivitas")
    for log in st.session_state.log_messages:
        st.write(log)