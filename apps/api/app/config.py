from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://permit:permit@localhost:5432/permit"
    qdrant_url: str = "http://localhost:6333"
    vworld_api_key: str | None = None


settings = Settings()
