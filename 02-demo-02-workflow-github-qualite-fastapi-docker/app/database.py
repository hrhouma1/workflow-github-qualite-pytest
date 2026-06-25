"""Configuration de la base de données (SQLAlchemy).

L'URL de connexion est lue depuis la variable d'environnement DATABASE_URL.
Par défaut, on pointe vers le service `db` (PostgreSQL) défini dans
docker-compose.yml. En test, cette dépendance est remplacée par SQLite.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/notesdb",
)

# create_engine n'ouvre PAS de connexion immédiatement : importer ce module
# ne nécessite donc pas qu'une base PostgreSQL soit disponible.
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """Fournit une session de base de données par requête (dépendance FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
