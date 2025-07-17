import time
import json
import ssl
from random import choice
import paho.mqtt.client as mqtt

# ——— Configuración MQTT (HiveMQ Cloud) ———
BROKER   = "ec6ee2c3428541a5b0c076d0aca0163e.s1.eu.hivemq.cloud"
PORT     = 8883
USERNAME = "tuki"  
PASSWORD = "tuki_password"  
TOPIC    = "forest/sensors"

def receive_from_lora():
    """Simula paquetes entrantes desde nodos LoRa."""
    return {
        "node_id": f"node_{choice(range(1,10))}",
        "ts":      int(time.time()),
        "temperature": 22.5,
        "humidity":    48.2,
        "co2":         420,
        "smoke":       0
    }

def main():
    # 1) Instancia del cliente MQTT
    client = mqtt.Client(client_id="gateway-1", protocol=mqtt.MQTTv311)

    # 2) Configuración TLS
    client.tls_set(
        ca_certs=None,             # usa las CAs del sistema
        certfile=None,
        keyfile=None,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
        ciphers=None
    )
    client.tls_insecure_set(False)

    # 3) Autenticación
    client.username_pw_set(USERNAME, PASSWORD)

    # 4) Conexión al broker HiveMQ Cloud
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            packet = receive_from_lora()
            payload = json.dumps(packet)
            # 5) Publicación segura con QoS=1
            client.publish(TOPIC, payload, qos=1)
            print(f"[GATEWAY] Reenviado: {payload}")
            time.sleep(5)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
