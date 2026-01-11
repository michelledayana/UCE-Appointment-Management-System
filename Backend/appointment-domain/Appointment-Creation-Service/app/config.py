from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_TOPIC_APPOINTMENT_CREATED: str = "appointment.created"

    # MQTT
    MQTT_BROKER: str = "hivemq"
    MQTT_PORT: int = 1883
    MQTT_TOPIC_APPOINTMENT_CREATED: str = "appointments/created"

    class Config:
        env_file = ".env"

settings = Settings()
