import json
import os
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from app.core.logger import logger

# Variable global para reutilizar el productor
_producer = None

def get_kafka_producer():
    """Crea el productor una sola vez (Singleton) con reintentos de conexión."""
    global _producer
    if _producer is None:
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        while True:
            try:
                _producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    retries=5,
                    acks='all'
                )
                logger.info("--- [LOG] Productor de Kafka conectado exitosamente ---")
                break
            except NoBrokersAvailable:
                logger.warning("--- [LOG] Kafka no disponible aún. Reintentando en 5s... ---")
                time.sleep(5)
    return _producer

def publish_user_registered_event(user_data: dict):
    """Publica el evento usando el productor global."""
    try:
        producer = get_kafka_producer()
        topic = "user_registered_topic"
        
        # Enviamos los datos
        producer.send(topic, user_data)
        producer.flush()
        
        logger.info(f"Evento publicado en '{topic}' para: {user_data.get('email')}")
    except Exception as e:
        logger.error(f"Error al publicar en Kafka: {str(e)}")