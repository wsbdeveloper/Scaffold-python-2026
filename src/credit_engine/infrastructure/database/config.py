"""Database Configuration"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configurações do banco de dados"""

    database_url: str = "postgresql://user:password@localhost:5432/credit_engine"
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",
        env_ignore_empty=False,
        env_nested_delimiter=None,
        env_nested_max_split=None,
        nested_model_default_partial_update=False,
    )


def get_database_url() -> str:
    """Retorna a URL do banco de dados"""
    settings = DatabaseSettings()
    return settings.database_url
