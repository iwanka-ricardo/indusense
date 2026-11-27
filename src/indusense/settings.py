"""Paramètres de l'application, lus depuis les variables d'environnement et `.env`.

Source unique de configuration technique : l'application et Alembic
construisent leur URL de connexion ici. Aucun identifiant n'est écrit en dur
ailleurs (ni dans alembic.ini, ni dans le code).
"""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # PostgreSQL (mêmes noms de variables que docker-compose.yml)
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "indusense_db"
    db_user: str = "indusense_user"
    db_password: SecretStr = SecretStr("dbpassword")

    # Clé de pseudonymisation HMAC-SHA-256 (SILVER, opération ANO)
    pseudonymization_key: SecretStr | None = None

    # API exposée sur l'hôte et scrapée par Prometheus
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
