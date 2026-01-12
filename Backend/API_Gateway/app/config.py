from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "API Gateway"

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # USER DOMAIN
    USER_REGISTRATION_URL: str
    AUTH_SERVICE_URL: str
    USER_PROFILE_URL: str

    # SERVICE DOMAIN
    SERVICE_CATALOG_URL: str

    # SCHEDULING DOMAIN
    SCHEDULING_MANAGEMENT_URL: str
    AVAILABILITY_SERVICE_URL: str

    # APPOINTMENT DOMAIN
    APPOINTMENT_CREATION_URL: str
    APPOINTMENT_MANAGEMENT_URL: str
    APPOINTMENT_QUERY_URL: str

    # ADMIN DOMAIN
    ADMINISTRATION_SERVICE_URL: str

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()
