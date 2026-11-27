"""Base déclarative SQLAlchemy partagée par tous les modèles.

Les modèles SQLAlchemy sont la source de vérité du schéma PostgreSQL :
Alembic compare `Base.metadata` à la base pour générer les migrations.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Schémas PostgreSQL du projet
SCHEMAS = ("meta", "bronze", "silver", "gold")

# Noms de contraintes stables : sans convention, les migrations
# autogénérées produisent des noms aléatoires difficiles à faire évoluer.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
