from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    service_name: str = "user-profile-service"

    database_url: str = Field(..., alias="DATABASE_URL")
    kafka_bootstrap_servers: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic_name: str = Field(..., alias="KAFKA_TOPIC_NAME")

    class Config:
        env_file = ".env"
        populate_by_name = True

settings = Settings()
