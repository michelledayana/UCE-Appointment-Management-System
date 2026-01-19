from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # =====================
    # APP
    # =====================
    app_name: str = Field(..., alias="APP_NAME")
    app_port: int = Field(..., alias="APP_PORT")
    environment: str = Field(..., alias="ENVIRONMENT")
    log_level: str = Field(..., alias="LOG_LEVEL")

    # =====================
    # DATABASE
    # =====================
    database_url: str = Field(..., alias="DATABASE_URL")
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")

    # =====================
    # KAFKA
    # =====================
    kafka_bootstrap_servers: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic_appointment_created: str = Field(
        ..., alias="KAFKA_TOPIC_APPOINTMENT_CREATED"
    )

    class Config:
        env_file = ".env"
        extra = "forbid"   # 🔥 explícito (enterprise)


settings = Settings()
