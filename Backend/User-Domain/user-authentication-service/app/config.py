from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    kafka_bootstrap_servers: str

    class Config:
        env_file = ".env"

settings = Settings()

# Compatibilidad con imports actuales
DATABASE_URL = settings.database_url
JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
JWT_EXPIRE_MINUTES = settings.jwt_expire_minutes
KAFKA_BOOTSTRAP_SERVERS = settings.kafka_bootstrap_servers
