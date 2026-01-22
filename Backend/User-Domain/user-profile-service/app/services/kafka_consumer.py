import json
import logging
from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import UserProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user-profile-consumer")


def consume_user_registered():
    consumer = KafkaConsumer(
        "user_registered_topic",
        bootstrap_servers="kafka:29092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="user-profile-service",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    logger.info("📡 Listening for user_registered events...")

    for message in consumer:
        data = message.value
        logger.info(f"📨 User registered event: {data}")

        db: Session = SessionLocal()

        try:
            email = data.get("email")
            full_name = data.get("full_name")
            user_type = data.get("user_type")

            if not email or not full_name or not user_type:
                logger.warning("⚠️ Invalid event data, skipping")
                continue

            existing = db.query(UserProfile).filter(
                UserProfile.email == email
            ).first()

            if existing:
                logger.info(f"ℹ️ Profile already exists: {email}")
                continue

            profile = UserProfile(
                email=email,
                full_name=full_name,
                user_type=user_type
            )

            db.add(profile)
            db.commit()
            db.refresh(profile)

            logger.info(f"✅ Profile created for {email}")

        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error creating profile: {e}")

        finally:
            db.close()
