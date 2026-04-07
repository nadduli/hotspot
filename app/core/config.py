from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    # ── App ───────────────────────────────────────
    APP_NAME: str = "Hotspot Payment Gateway"
    DEBUG: bool = False
    SECRET_KEY: str                        # for signing sessions/tokens

    # ── Database ──────────────────────────────────
    DATABASE_URL: str                      # postgresql+asyncpg://...

    # ── MikroTik ──────────────────────────────────
    MIKROTIK_DEFAULT_PORT: int = 8728
    MIKROTIK_DEFAULT_USER: str = "api_user"

    # ── iotec Payment ─────────────────────────────
    IOTEC_BASE_URL: str
    IOTEC_API_KEY: str
    IOTEC_API_SECRET: str
    IOTEC_MERCHANT_CODE: str
    IOTEC_WEBHOOK_SECRET: str              # for verifying callbacks

    # ── Admin ─────────────────────────────────────
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str                    # no default — must be set explicitly

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()