import json
from kafka import KafkaConsumer
from app.config import settings


def iniciar_consumidor():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC_NAME,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="auth-service-group",
        auto_offset_reset="earliest"
    )

    print("👂 Kafka consumer started (Auth Service)")

    for message in consumer:
        data = message.value
        print("📨 User registered event received:", data)
