from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://localhost:8082"
    USER_SERVICE_URL: str = "http://localhost:8081"
    APPOINTMENT_SERVICE_URL: str = "http://localhost:8083"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
