from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_APPOINTMENT_TOPIC: str = "appointment.created"

    class Config:
        env_file = ".env"

settings = Settings()
