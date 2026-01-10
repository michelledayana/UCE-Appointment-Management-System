from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    MQTT_BROKER: str = "hivemq"
    MQTT_PORT: int = 1883

settings = Settings()
