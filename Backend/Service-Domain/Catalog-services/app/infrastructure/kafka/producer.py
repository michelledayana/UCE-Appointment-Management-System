import json
from kafka import KafkaProducer
from app.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_SERVICE_EVENTS

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_service_event(event_type: str, payload: dict):
    event = {
        "event_type": event_type,
        "payload": payload
    }
    producer.send(KAFKA_TOPIC_SERVICE_EVENTS, event)
    producer.flush()
