import json
import logging
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from app.config.settings import settings
from app.db.database import SessionLocal
from app.models.user import UserProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consume_user_registered():
    while True:
        try:
            consumer = KafkaConsumer(
                settings.kafka_topic_name,
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                group_id="user-profile-group",
                auto_offset_reset="earliest",
                enable_auto_commit=True
            )

            logger.info(
                f"Listening to topic {settings.kafka_topic_name}"
            )

            for message in consumer:
                user_data = message.value
                logger.info(f"Event received: {user_data}")

                db = SessionLocal()
                try:
                    exists = db.query(UserProfile).filter(
                        UserProfile.email == user_data["email"]
                    ).first()

                    if exists:
                        logger.info("Profile already exists")
                        continue

                    profile = UserProfile(
                        email=user_data["email"],
                        full_name=user_data["full_name"],
                        user_type=user_data.get("user_type", "GENERAL")
                    )

                    db.add(profile)
                    db.commit()

                    logger.info(
                        f"Profile created for {profile.email}"
                    )

                except Exception as e:
                    db.rollback()
                    logger.error(f"DB error: {e}")
                finally:
                    db.close()

        except NoBrokersAvailable:
            logger.warning("Kafka not ready, retrying in 5s...")
            time.sleep(5)
