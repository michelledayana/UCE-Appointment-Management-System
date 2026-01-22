from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    app_name: str = "Scheduling Management Service"
    environment: str = "qa"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8085

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    cors_origins: str = "*"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
