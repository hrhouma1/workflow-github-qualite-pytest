"""Fixtures de test : application Flask sur base SQLite isolée.

On configure une base SQLite **en mémoire** partagée via `StaticPool`
(sinon chaque connexion créerait sa propre base vide). Aucun PostgreSQL
n'est nécessaire pour exécuter les tests.
"""

import pytest
from sqlalchemy.pool import StaticPool

from app import create_app


@pytest.fixture()
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        },
    }
    return create_app(test_config)


@pytest.fixture()
def client(app):
    return app.test_client()
