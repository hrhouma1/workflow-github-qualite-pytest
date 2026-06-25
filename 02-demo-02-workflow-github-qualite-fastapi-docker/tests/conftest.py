"""Fixtures de test : base SQLite isolée + client HTTP FastAPI.

On remplace la dépendance `get_db` (PostgreSQL en production) par une base
SQLite en mémoire. Les tests ne nécessitent donc AUCUN service externe :
ils tournent tels quels dans la CI, sans conteneur PostgreSQL.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # On n'utilise PAS `with TestClient(...)` afin de ne pas déclencher le
    # lifespan (qui tenterait de créer les tables sur le moteur PostgreSQL).
    yield TestClient(app)
    app.dependency_overrides.clear()
