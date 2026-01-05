from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # 🔑 evita errores por variables extra
    )

settings = Settings()

settings = Settings()
