"""Package applicatif de l'API Flask (démo 03).

Utilise le patron "application factory" (`create_app`) et Flask-SQLAlchemy
pour persister les évaluations dans PostgreSQL via Docker Compose.
"""

import os

from flask import Flask

from app.extensions import db


def create_app(config: dict | None = None) -> Flask:
    """Crée et configure l'application Flask.

    Args:
        config: surcharge de configuration (utilisée notamment par les tests
            pour pointer vers une base SQLite en mémoire).
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/notesdb",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    from app.routes import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
