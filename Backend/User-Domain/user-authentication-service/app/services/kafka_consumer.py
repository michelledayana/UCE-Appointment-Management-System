import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from app.config import settings
from app.store.user_store import users


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

        # 🔐 Validación del evento
        if not REQUIRED_FIELDS.issubset(data):
            print("❌ Invalid Kafka event:", data)
            continue

        email = data["email"]

        if email in users:
            print(f"⚠️ User already in memory: {email}")
            continue

        users[email] = {
            "password_hash": data["password_hash"],
            "user_type": data["user_type"]
        }

        print(f"✅ User loaded into memory: {email}")
