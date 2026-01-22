from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # ==========================
    # APP
    # ==========================
    APP_NAME: str
    APP_PORT: int
    ENVIRONMENT: str = "local"

    # ==========================
    # DATABASE
    # ==========================
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DATABASE_URL: str

    # ==========================
    # KAFKA
    # ==========================
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_APPOINTMENT_CREATED: str
    KAFKA_TOPIC_SERVICE_EVENTS: str

    # ==========================
    # MQTT
    # ==========================
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_TOPIC_APPOINTMENT_CREATED: str

    # ==========================
    # LOGGING
    # ==========================
    LOG_LEVEL: str = "INFO"

    # ✅ Pydantic v2 config
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"   # 🔥 clave para pytest
    )


settings = Settings()
