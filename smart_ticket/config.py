# smart_ticket/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    api_base: str = "https://sandbox.ticketplatform.com/v1"

    # 给出占位默认值，测试环境无需真 Token；生产可用环境变量覆盖
    api_token: str = Field(default="DUMMY", env="API_TOKEN")

    request_timeout: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
