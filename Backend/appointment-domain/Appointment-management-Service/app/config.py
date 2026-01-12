from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # APP
    # ==========================
    APP_NAME: str = Field(..., alias="APP_NAME")
    APP_PORT: int = Field(..., alias="APP_PORT")
    ENVIRONMENT: str = Field(..., alias="ENVIRONMENT")

    # ==========================
    # DATABASE
    # ==========================
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    DB_HOST: str = Field(..., alias="DB_HOST")
    DB_PORT: int = Field(..., alias="DB_PORT")
    DB_NAME: str = Field(..., alias="DB_NAME")
    DB_USER: str = Field(..., alias="DB_USER")
    DB_PASSWORD: str = Field(..., alias="DB_PASSWORD")

    # ==========================
    # KAFKA
    # ==========================
    KAFKA_BOOTSTRAP_SERVERS: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC_APPOINTMENT_CREATED: str = Field(..., alias="KAFKA_TOPIC_APPOINTMENT_CREATED")

    # ==========================
    # LOGGING
    # ==========================
    LOG_LEVEL: str = Field("INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
