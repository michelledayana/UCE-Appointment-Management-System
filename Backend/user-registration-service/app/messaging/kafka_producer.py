import json
from kafka import KafkaProducer

def publish_user_registered_event(user):
    try:
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        event = {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type
        }

        producer.send("user-registered", event)
        producer.flush()

    except Exception:
        # Kafka NO es obligatorio
        pass
