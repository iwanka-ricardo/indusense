"""create schemas

Revision ID: 0001
Revises: 
Create Date: 2026-11-27 18:41:10.379585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# `meta` est créé par env.py (il héberge la table de version d'Alembic) :
# il n'est donc ni créé ni supprimé ici.
LAYER_SCHEMAS = ("bronze", "silver", "gold")


def upgrade() -> None:
    """Crée les schémas des couches BRONZE, SILVER et GOLD."""
    for schema in LAYER_SCHEMAS:
        op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")


def downgrade() -> None:
    """Supprime les schémas, uniquement s'ils sont vides (pas de CASCADE : aucune perte de données)."""
    for schema in reversed(LAYER_SCHEMAS):
        op.execute(f"DROP SCHEMA IF EXISTS {schema} RESTRICT")
