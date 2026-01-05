from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "appointment-service"
    SERVICE_PORT: int = 8083

    class Config:
        env_file = ".env"


settings = Settings()
