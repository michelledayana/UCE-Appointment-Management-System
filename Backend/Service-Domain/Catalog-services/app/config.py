import os

# =========================
# Service
# =========================
SERVICE_NAME = os.getenv("SERVICE_NAME", "catalog-service")

# =========================
# MongoDB
# =========================
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb_catalog")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB_NAME = os.getenv("MONGO_DB", "catalog_db")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

# =========================
# Redis
# =========================
REDIS_HOST = os.getenv("REDIS_HOST", "redis_catalog")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# =========================
# Kafka
# =========================
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"
)
KAFKA_TOPIC_SERVICE_EVENTS = os.getenv(
    "KAFKA_TOPIC_SERVICE_EVENTS", "service_events"
)
