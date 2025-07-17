import json
import ssl
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
from alert_service import notify_if_needed

# ——— Configuración MQTT (HiveMQ Cloud) ———
BROKER   = "ec6ee2c3428541a5b0c076da0ca0163e.s1.eu.hivemq.cloud"
PORT     = 8883
USERNAME = "manuel"
PASSWORD = "Al24092002"
TOPIC    = "forest/sensors"

# ——— Configuración InfluxDB ———
INFLUX_HOST = 'localhost'
INFLUX_PORT = 8086
DB_NAME     = 'forest_monitor'

# ——— Umbrales de alerta ———
THRESHOLDS = {
    "temperature":  45.0,
    "humidity":     15.0,
    "co2":          1000,
    "smoke":        1
}

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)
    print(f"[SERVER] Conectado y suscrito a {TOPIC}")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    # Montar punto InfluxDB
    point = [{
        "measurement": "sensor_readings",
        "tags": {"node_id": payload["node_id"]},
        "time": payload["ts"] * 1_000_000_000,  # nanosegundos
        "fields": {
            "temperature": float(payload["temperature"]),
            "humidity":    float(payload["humidity"]),
            "co2":         float(payload["co2"]),
            "smoke":       int(payload["smoke"])
        }
    }]
    influx.write_points(point)
    print(f"[SERVER] Almacenado: {payload}")

    # Comprobar umbrales
    alerts = [k for k,v in payload.items() if k in THRESHOLDS and payload[k] >= THRESHOLDS[k]]
    if alerts:
        notify_if_needed(payload["node_id"], payload["ts"], alerts)

if __name__ == "__main__":
    # 1) Inicializa InfluxDB
    influx = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, database=DB_NAME)
    influx.create_database(DB_NAME)

    # 2) Inicializa cliente MQTT
    client = mqtt.Client(client_id="server-ingest", protocol=mqtt.MQTTv311)

    # 3) TLS y autenticación
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.tls_insecure_set(True)
    client.username_pw_set(USERNAME, PASSWORD)

    # 4) Callbacks y conexión
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)

    # 5) Escucha mensajes
    client.loop_forever()
