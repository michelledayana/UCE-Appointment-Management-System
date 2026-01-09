class Settings(BaseSettings):
    # App
    app_name: str = "User Registration Service"

    # Database
    database_url: str

    # Kafka
    kafka_bootstrap_servers: str | None = None
    kafka_topic_name: str = "user_registered_topic"  # 👈 renombrado

    class Config:
        env_file = ".env"
        extra = "ignore"
