"""Database Configuration"""
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Configurações do banco de dados"""
    database_url: str = "postgresql://user:password@localhost:5432/credit_engine"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file


def get_database_url() -> str:
    """Retorna a URL do banco de dados"""
    settings = DatabaseSettings()
    return settings.database_url

