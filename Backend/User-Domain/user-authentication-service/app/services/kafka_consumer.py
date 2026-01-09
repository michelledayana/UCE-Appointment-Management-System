import json
from kafka import KafkaConsumer
from app.config import settings

def iniciar_consumidor():
    consumer = KafkaConsumer(
        "user_registered_topic",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="auth-service-group"
    )

    for message in consumer:
        print("User registered event:", message.value)
