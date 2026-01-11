import os

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb_admin:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "admin_db")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_EVENTS = os.getenv("KAFKA_TOPIC_EVENTS")


