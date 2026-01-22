import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from app.config import settings
from app.database.db import SessionLocal
from app.models.auth_model import AuthUser

REQUIRED_FIELDS = {"email", "password_hash", "user_type"}


def iniciar_consumidor():
    while True:
        try:
            consumer = KafkaConsumer(
                settings.KAFKA_TOPIC_NAME,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                group_id="auth-service-group",
                auto_offset_reset="earliest"
            )
            print("👂 Kafka consumer connected successfully")
            break
        except NoBrokersAvailable:
            print("⏳ Kafka not available yet, retrying in 5 seconds...")
            time.sleep(5)

    for message in consumer:
        data = message.value

        if not REQUIRED_FIELDS.issubset(data):
            print("❌ Invalid Kafka event:", data)
            continue

        db = SessionLocal()
        try:
            exists = db.query(AuthUser).filter(
                AuthUser.email == data["email"]
            ).first()

            if exists:
                print(f"⚠️ User already exists in auth DB: {data['email']}")
                continue

            user = AuthUser(
                email=data["email"],
                password_hash=data["password_hash"],
                user_type=data["user_type"]
            )

            db.add(user)
            db.commit()

            print(f"✅ User saved in auth DB: {user.email}")

        except Exception as e:
            db.rollback()
            print("❌ Error saving auth user:", e)

        finally:
            db.close()
