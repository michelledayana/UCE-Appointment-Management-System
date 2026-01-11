import json
from kafka import KafkaProducer
from app.config import settings

producer = None

def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    return producer

def publish_appointment_created(event: dict):
    try:
        producer = get_producer()
        producer.send(
            settings.KAFKA_TOPIC_APPOINTMENT_CREATED,
            event
        )
        producer.flush()
    except Exception as e:
        print("⚠ Kafka not available:", e)
