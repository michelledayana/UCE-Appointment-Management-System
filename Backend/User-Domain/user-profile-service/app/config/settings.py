from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    service_name: str = "user-profile-service"

    class Config:
        env_file = ".env"


settings = Settings()
