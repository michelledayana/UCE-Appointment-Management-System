import json
import os
from kafka import KafkaProducer

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS",
                "kafka:9092"
            ),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            request_timeout_ms=30000
        )
    return _producer


def publish_service_event(event_type: str, payload: dict):
    event = {
        "event_type": event_type,
        "payload": payload
    }

    producer = get_producer()
    producer.send(
        os.getenv("KAFKA_TOPIC_SERVICE_EVENTS", "service-events"),
        event
    )
    producer.flush()
