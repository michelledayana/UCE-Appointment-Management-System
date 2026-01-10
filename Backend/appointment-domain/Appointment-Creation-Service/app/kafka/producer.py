import json
from kafka import KafkaProducer
from app.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode()
)

def publish_appointment_created(event: dict):
    producer.send("appointment_created", event)
