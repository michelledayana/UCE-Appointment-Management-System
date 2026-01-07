import json
from kafka import KafkaProducer
import logging

logger = logging.getLogger("user-registration")

# Initialize producer (adjust bootstrap_servers if needed)
try:
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    logger.error(f"Failed to initialize Kafka Producer: {e}")

def publish_user_registered_event(data):
    try:
        producer.send('user_registered_topic', value=data)
        producer.flush()
        logger.info(f"Event published for user: {data['email']}")
    except Exception as e:
        logger.error(f"Error publishing to Kafka: {str(e)}")
        # We don't raise the error so the HTTP response can still succeed