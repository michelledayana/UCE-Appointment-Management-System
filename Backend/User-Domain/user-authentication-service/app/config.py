from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = settings.DATABASE_URL
