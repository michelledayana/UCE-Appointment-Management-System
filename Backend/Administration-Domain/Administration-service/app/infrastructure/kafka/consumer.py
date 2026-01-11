import json
from kafka import KafkaConsumer
from app.config import KAFKA_BOOTSTRAP_SERVERS
from app.application.handlers.event_handlers import handle_event

def start_kafka_consumer():
    consumer = KafkaConsumer(
        "user_registered_topic",
        "appointment-events",
        "appointment_created",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        group_id="administration-service"
    )

    for message in consumer:
        event_data = message.value
        handle_event(event_data)
