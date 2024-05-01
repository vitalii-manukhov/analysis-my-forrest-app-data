"""Get environment variables"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: int = -1
    DB_NAME: str = "postgres"
    DB_DEFAULT_NAME: str = "postgres"
    DB_TABLE_NAME: str = '_'

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="allow")

    @property
    def get_db_url_psycopg(self):
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
# print(settings.model_dump())
