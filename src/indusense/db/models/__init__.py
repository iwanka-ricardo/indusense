"""Import de tous les modèles pour qu'ils soient enregistrés dans Base.metadata.

Alembic importe ce module : tout nouveau fichier de modèles doit être ajouté ici.
"""

from indusense.db.models import bronze, gold, meta, silver  # noqa: F401
