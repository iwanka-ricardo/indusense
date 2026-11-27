"""Environnement Alembic d'Indusense.

- L'URL de connexion vient de `indusense.settings` (fichier .env), jamais d'alembic.ini.
- La cible est `Base.metadata` : les modèles SQLAlchemy sont la source de vérité.
- Seuls les schémas du projet (meta, bronze, silver, gold) sont comparés.
- La table de version d'Alembic est rangée dans le schéma `meta`.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, text

import indusense.db.models  # noqa: F401  (enregistre les modèles dans Base.metadata)
from indusense.db.base import SCHEMAS, Base
from indusense.settings import get_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option(
    "sqlalchemy.url",
    get_settings().database_url.render_as_string(hide_password=False).replace("%", "%%"),
)

target_metadata = Base.metadata

VERSION_TABLE_SCHEMA = "meta"


def include_name(name, type_, parent_names):
    """Ne compare que les schémas du projet (ignore public et les schémas système)."""
    if type_ == "schema":
        return name in SCHEMAS
    return True


def _configure(**kwargs) -> None:
    context.configure(
        target_metadata=target_metadata,
        include_schemas=True,
        include_name=include_name,
        version_table_schema=VERSION_TABLE_SCHEMA,
        compare_type=True,
        **kwargs,
    )


def run_migrations_offline() -> None:
    """Génère le SQL sans connexion (`alembic upgrade head --sql`)."""
    _configure(url=config.get_main_option("sqlalchemy.url"), literal_binds=True)
    with context.begin_transaction():
        context.execute(f"CREATE SCHEMA IF NOT EXISTS {VERSION_TABLE_SCHEMA}")
        context.run_migrations()


def run_migrations_online() -> None:
    """Applique les migrations sur la base (`make migrate`)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        # La table de version vit dans `meta` : le schéma doit exister avant.
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {VERSION_TABLE_SCHEMA}"))
        connection.commit()
        _configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
