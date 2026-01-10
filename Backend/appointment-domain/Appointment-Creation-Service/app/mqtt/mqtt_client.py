import json
import paho.mqtt.client as mqtt
from app.config import settings

client = mqtt.Client()
client.connect(settings.MQTT_BROKER, settings.MQTT_PORT)

def publish_notification(event: dict):
    client.publish(
        "appointments/created",
        json.dumps(event)
    )
