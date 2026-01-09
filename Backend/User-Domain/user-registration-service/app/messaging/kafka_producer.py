import json
import logging
from kafka import KafkaProducer
from app.config import settings

logger = logging.getLogger("user-registration")

producer = None

# Inicializar Kafka SOLO si hay bootstrap servers
if settings.kafka_bootstrap_servers:
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
        )
        logger.info("Kafka producer initialized")
    except Exception as e:
        logger.error(f"Kafka producer not available: {e}")
else:
    logger.warning("Kafka bootstrap servers not configured, producer disabled")


def publish_user_registered_event(data: dict):
    if not producer:
        logger.warning("Kafka producer not ready, event skipped")
        return

    producer.send(settings.kafka_user_topic, value=data)
    producer.flush()

    logger.info(f"Event published for user: {data['email']}")
