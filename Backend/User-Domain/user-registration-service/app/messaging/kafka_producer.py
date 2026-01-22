import json
import logging
from kafka import KafkaProducer
from app.config import settings

logger = logging.getLogger("user-registration")
producer = None

def init_kafka():
    global producer
    if not settings.kafka_bootstrap_servers:
        logger.warning("Kafka bootstrap servers not configured")
        return

    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
        )
        logger.info("Kafka producer initialized")
    except Exception as e:
        logger.error(f"Kafka producer not available: {e}")

def publish_user_registered_event(data: dict):
    if not producer:
        logger.warning("Kafka producer not ready, event skipped")
        return

    try:
        producer.send(settings.kafka_topic_name, value=data)
        producer.flush()
        logger.info(f"Event published for user: {data['email']}")
    except Exception as e:
        logger.error(f"Failed to publish Kafka event: {e}")

# Inicializamos producer al importar
init_kafka()
