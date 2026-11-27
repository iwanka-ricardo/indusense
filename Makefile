# Indusense - commandes du projet. `make help` pour la liste.
.DEFAULT_GOAL := help
.PHONY: help env up down ps logs migrate revision bronze api test

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

env: ## Crée .env à partir de .env.example (sans écraser un .env existant)
	@test -f .env && echo ".env existe déjà" || (cp .env.example .env && echo ".env créé : pense à changer les mots de passe")

# --- Infrastructure (Docker Compose) ---------------------------------------
up: ## Démarre les services (db, pgAdmin, Prometheus, Alertmanager, Grafana)
	docker compose up -d

down: ## Arrête et supprime les conteneurs (les volumes sont conservés)
	docker compose down

ps: ## État des conteneurs
	docker compose ps

logs: ## Logs des services (make logs s=db pour un seul service)
	docker compose logs -f $(s)

# --- Schéma de base (Alembic, seule source de vérité) ----------------------
migrate: ## Applique les migrations Alembic
	uv run alembic upgrade head

revision: ## Génère une migration depuis les modèles (make revision m="message")
	uv run alembic revision --autogenerate -m "$(m)"

# --- Pipeline ---------------------------------------------------------------
bronze: ## Ingestion BRONZE
	uv run python -m indusense.cli bronze

api: ## Lance l'API sur l'hôte (scrapée par Prometheus)
	uv run python -m indusense.api.main

test: ## Lance les tests
	uv run pytest
