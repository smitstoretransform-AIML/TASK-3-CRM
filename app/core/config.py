from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SMTP / Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"

    SMTP_PORT: int = 587

    SMTP_USERNAME: str

    SMTP_PASSWORD: str

    SMTP_FROM_EMAIL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

