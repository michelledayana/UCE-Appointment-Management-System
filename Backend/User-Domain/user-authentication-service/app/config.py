from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_NAME: str

    model_config = ConfigDict(
        env_file=".env",
        extra="allow"   # 👈 ESTA ES LA CLAVE
    )


settings = Settings()

# Export for SQLAlchemy
DATABASE_URL = settings.DATABASE_URL
