import os

# ===============================
# SERVICE
# ===============================
SERVICE_NAME = os.getenv("SERVICE_NAME", "administration-service")

# ===============================
# MongoDB
# ===============================
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb_admin")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "admin_db")
MONGO_URI = os.getenv(
    "MONGO_URI",
    f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
)

# ===============================
# Kafka
# ===============================
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC_EVENTS = os.getenv("KAFKA_TOPIC_EVENTS", "system_events")
