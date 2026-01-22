import json
from kafka import KafkaConsumer
from app.config import KAFKA_BOOTSTRAP_SERVERS
from app.application.handlers.event_handlers import handle_event

def process_message(event_data: dict):
    handle_event(event_data)

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
        process_message(message.value)
