from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===============================
    # APPLICATION
    # ===============================
    SERVICE_NAME: str
    ENVIRONMENT: str

    # ===============================
    # SERVER
    # ===============================
    HOST: str
    PORT: int

    # ===============================
    # DATABASE
    # ===============================
    DATABASE_URL: str

    # ===============================
    # KAFKA
    # ===============================
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_USER_REGISTERED: str
    KAFKA_CONSUMER_GROUP: str

    KAFKA_SESSION_TIMEOUT_MS: int = 10000
    KAFKA_REQUEST_TIMEOUT_MS: int = 40000

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
