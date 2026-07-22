from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===========================
    # Database
    # ===========================
    DATABASE_URL: str

    # ===========================
    # Environment
    # ===========================
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    ENABLE_JOB_SCHEDULER: bool = False

    # ===========================
    # JWT
    # ===========================
    JWT_SECRET_KEY: str

    JWT_ACCESS_TOKEN_MINUTES: int = 15
    JWT_REFRESH_TOKEN_DAYS: int = 7

    # ===========================
    PASSWORD_RESET_TOKEN_MINUTES: int = 30

    MAX_RESUME_SIZE_BYTES: int = 5 * 1024 * 1024

    # ===========================
    # Frontend / Backend
    # ===========================
    FRONTEND_URL: str
    BACKEND_URL: str

    # Gmail SMTP (use a Gmail App Password, never the account password)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""

    # ===========================
    # CORS
    # ===========================
    CORS_ORIGINS: str

    # ===========================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

if settings.ENVIRONMENT.lower() == "production" and len(settings.JWT_SECRET_KEY) < 32:
    raise RuntimeError("Production requires a JWT secret of at least 32 characters.")
