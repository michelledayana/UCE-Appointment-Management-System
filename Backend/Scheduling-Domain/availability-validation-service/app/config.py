from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "redis_catalog"
    REDIS_PORT: int = 6379
    MONGO_URI: str = "mongodb://54.88.248.219:27017/availability_db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
MONGO_URI = settings.MONGO_URI
