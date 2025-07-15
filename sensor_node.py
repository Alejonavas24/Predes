import time
import json
import random
import ssl
import paho.mqtt.client as mqtt

# ——— Configuración MQTT (HiveMQ Cloud) ———
BROKER   = "ec6ee2c3428541a5b0c076d0aca0163e.s1.eu.hivemq.cloud"
PORT     = 8883                              # TLS port
USERNAME = ""               # pon aquí tu usuario del dashboard
PASSWORD = "a"               # pon aquí tu contraseña del dashboard
TOPIC    = "forest/sensors"

def read_sensors():
    """Simula lectura de sensores: temperatura, humedad, CO2 y humo."""
    return {
        "temperature": 20 + random.uniform(-5, 5),
        "humidity":    50 + random.uniform(-20, 20),
        "co2":         400 + random.uniform(-100, 500),
        "smoke":       random.randint(0, 1)
    }

def main():
    # 1) Creamos el cliente MQTT
    client = mqtt.Client(client_id="sensor-node-1", protocol=mqtt.MQTTv311)

    # 2) Configuramos TLS para cifrar la conexión
    client.tls_set(         # usa las CAs por defecto del sistema
        ca_certs=None,
        certfile=None,
        keyfile=None,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
        ciphers=None
    )
    client.tls_insecure_set(False)  # asegurar validación de certificado

    # 3) Autenticación con usuario/clave
    client.username_pw_set(USERNAME, PASSWORD)

    # 4) Conectamos al broker HiveMQ Cloud
    client.connect(BROKER, PORT, keepalive=60)

    # 5) Iniciamos el loop en background para gestionar reconexiones y callbacks
    client.loop_start()

    try:
        while True:
            data = read_sensors()
            payload = json.dumps({
                "node_id": f"node_{random.randint(1,100)}",
                "ts":      int(time.time()),
                **data
            })
            # 6) Publicamos por TLS en el topic seguro
            client.publish(TOPIC, payload, qos=1)
            print(f"[SENSOR] Publicado: {payload}")
            time.sleep(60)  # espera 1 minuto entre lecturas
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
