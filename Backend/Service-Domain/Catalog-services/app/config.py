import os

# =========================
# Service
# =========================
SERVICE_NAME = os.getenv("SERVICE_NAME", "catalog-service")

# =========================
# MongoDB
# =========================
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB", "catalog_db")

# =========================
# Redis
# =========================
REDIS_HOST = os.getenv("REDIS_HOST", "redis_catalog")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))  # base por defecto 0

# =========================
# Kafka
# =========================
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"
)
KAFKA_TOPIC_SERVICE_EVENTS = os.getenv(
    "KAFKA_TOPIC_SERVICE_EVENTS", "service_events"
)
