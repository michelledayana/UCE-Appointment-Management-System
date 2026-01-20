import os

# ===============================
# SERVICE
# ===============================
SERVICE_NAME = os.getenv("SERVICE_NAME", "administration-service")

# ===============================
# MongoDB
# ===============================
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "admin_db")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is required. "
        "Define it in the environment variables."
    )

# ===============================
# Kafka
# ===============================
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092"
)

KAFKA_TOPIC_EVENTS = os.getenv(
    "KAFKA_TOPIC_EVENTS",
    "system_events"
)
