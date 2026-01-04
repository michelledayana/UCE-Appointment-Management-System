from kafka import KafkaProducer
import json
import os

producer = None

def get_producer():
    global producer
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=3
            )
        except Exception as e:
            print("⚠️ Kafka not available:", e)
            producer = None
    return producer


def send_event(topic: str, message: dict):
    prod = get_producer()
    if prod:
        prod.send(topic, message)
        prod.flush()
