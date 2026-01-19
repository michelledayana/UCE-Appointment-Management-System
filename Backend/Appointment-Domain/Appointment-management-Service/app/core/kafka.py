import json
import threading
import logging
from kafka import KafkaConsumer
from pydantic import ValidationError

from app.config import settings
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.schemas.appointment_event import AppointmentCreatedEvent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def start_consumer():
    logger.info("🚀 Starting Kafka consumer: appointment_created")

    consumer = KafkaConsumer(
        settings.kafka_topic_appointment_created,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="appointment-management-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: m.decode("utf-8"),
    )

    for message in consumer:
        raw_value = message.value.strip()

        # 🔥 IGNORAR MENSAJES VACÍOS
        if not raw_value:
            logger.warning("⚠️ Empty Kafka message ignored")
            continue

        try:
            payload = json.loads(raw_value)
        except json.JSONDecodeError:
            logger.error(f"❌ Invalid JSON ignored: {raw_value}")
            continue

        try:
            event = AppointmentCreatedEvent(**payload)
        except ValidationError as e:
            logger.error(f"❌ Invalid event schema: {e}")
            continue

        db = SessionLocal()
        try:
            appointment = Appointment(
                id=event.id,
                user_id=event.user_id,
                service_id=event.service_id,
                scheduled_time=event.scheduled_time,
                status=event.status
            )

            db.merge(appointment)
            db.commit()

            logger.info(
                f"📥 Appointment synced | id={event.id} status={event.status}"
            )

        except Exception as e:
            db.rollback()
            logger.error(f"❌ DB error: {e}", exc_info=True)
        finally:
            db.close()


def run_kafka_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
