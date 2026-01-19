import json
import paho.mqtt.client as mqtt
from app.config import settings

client = mqtt.Client()
_connected = False

def connect_mqtt():
    global _connected
    try:
        client.connect(
            settings.MQTT_BROKER,
            settings.MQTT_PORT,
            60
        )
        _connected = True
    except Exception as e:
        print("⚠ MQTT not available:", e)

def publish_appointment_created(event: dict):
    if not _connected:
        return
    try:
        payload = json.dumps(event)
        client.publish(
            settings.MQTT_TOPIC_APPOINTMENT_CREATED,
            payload
        )
    except Exception as e:
        print("⚠ MQTT publish error:", e)
