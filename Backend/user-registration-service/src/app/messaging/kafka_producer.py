from kafka import KafkaProducer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, USER_REGISTERED_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_user_registered_event(user):
    event = {
        "user_id": str(user.id),
        "email": user.email,
        "is_student": user.is_student
    }
    producer.send(USER_REGISTERED_TOPIC, event)
