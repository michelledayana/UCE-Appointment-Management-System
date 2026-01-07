import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Lee la variable de entorno que pusimos en el docker-compose o .env
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db-auth:5432/auth_db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

settings = Settings()

# Para que la importación 'from app.config import DATABASE_URL' funcione:
DATABASE_URL = settings.DATABASE_URL
