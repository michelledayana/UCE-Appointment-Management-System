from kafka import KafkaConsumer
import json
import logging
import os
import time
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 🔹 DEFINICIÓN GLOBAL
SERVICE_CACHE: Dict[str, Any] = {}

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
SERVICE_EVENTS_TOPIC = "service-events"


def safe_json_deserializer(value):
    if value is None:
        return None
    try:
        return json.loads(value.decode("utf-8"))
    except json.JSONDecodeError:
        logger.warning("⚠️ Invalid JSON received")
        return None


def start_catalog_consumer():
    logger.info("🔥 Kafka consumer starting with retry...")

    while True:
        try:
            consumer = KafkaConsumer(
                SERVICE_EVENTS_TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                group_id="appointment-creation-service",
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=safe_json_deserializer,
                request_timeout_ms=40000,
                session_timeout_ms=30000,
            )
            break
        except Exception as e:
            logger.error(f"❌ Kafka not available yet: {e}")
            time.sleep(5)

    logger.info("📥 Connected to Kafka. Listening to service-events...")

    for message in consumer:
        event = message.value
        if not event:
           continue

        logger.info(f"📩 Event received: {event}")

        if event.get("event_type") == "service.created":
            service_id = event.get("service_id")
            if service_id:
               SERVICE_CACHE[service_id] = event
               logger.info(f"🧠 Service cached: {service_id}")
            logger.info("✅ Service created event processed")

