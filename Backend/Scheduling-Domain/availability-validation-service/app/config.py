from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "redis_catalog"
    REDIS_PORT: int = 6379
    MONGO_URI: str = "mongodb://mongodb_catalog:27017/availability_db"

    class Config:
        env_file = ".env"


settings = Settings()

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
MONGO_URI = settings.MONGO_URI
