from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import HTTPException, Header, status


def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return x_api_key


class Settings(BaseSettings):
    api_key: str = "dev-key-please-set-API_KEY-env-var"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
