from pydantic_settings import BaseSettings

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

    class Config:
        env_file = ".env"

settings = Settings()
