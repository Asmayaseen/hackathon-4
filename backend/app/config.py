from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str

    # Cloudflare R2
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str = "course-companion-content"

    # App
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    UPGRADE_URL: str = "https://course-companion.fly.dev/upgrade"

    # Phase 2 — Hybrid Intelligence
    ANTHROPIC_API_KEY: str = ""  # Required for Phase 2 hybrid features

    # Course config
    FREE_TIER_MAX_CHAPTER: int = 3  # Chapters 1–3 are free


settings = Settings()
