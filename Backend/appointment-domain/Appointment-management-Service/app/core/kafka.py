import json
import threading
from kafka import KafkaConsumer
from app.config import settings
from app.db.session import SessionLocal
from app.models.appointment import Appointment


def start_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_APPOINTMENT_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="appointment-management-group",
        auto_offset_reset="earliest"
    )

    for message in consumer:
        event = message.value

        db = SessionLocal()
        try:
            appointment = Appointment(
                id=event["id"],
                user_id=event["user_id"],
                service_id=event["service_id"],
                scheduled_time=event["scheduled_time"],
                status=event["status"]
            )
            db.merge(appointment)
            db.commit()
        finally:
            db.close()


def run_kafka_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
