import json
from kafka import KafkaConsumer
from app.config import settings
from app.database.db import SessionLocal
from app.models.auth_model import AuthUser


def iniciar_consumidor():
    consumer = KafkaConsumer(
        "user_registered_topic",
        bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="auth-service-group",
        auto_offset_reset="earliest"
    )

    print("👂 Kafka consumer started (Auth Service)")

    for message in consumer:
        data = message.value
        print("📨 User registered event:", data)

        db = SessionLocal()
        try:
            # Evitar duplicados
            existing = db.query(AuthUser).filter(
                AuthUser.email == data["email"]
            ).first()

            if existing:
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
            print("❌ Error saving user in auth DB:", e)

        finally:
            db.close()
