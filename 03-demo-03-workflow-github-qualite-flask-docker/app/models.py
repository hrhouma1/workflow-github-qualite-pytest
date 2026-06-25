"""Modèle ORM Flask-SQLAlchemy."""

from datetime import datetime, timezone

from app.extensions import db


class Evaluation(db.Model):
    """Une évaluation persistée : les notes saisies et leur résultat calculé."""

    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)
    # Les notes sont stockées en CSV pour rester simple (ex : "80,90,100").
    notes = db.Column(db.String, nullable=False)
    moyenne = db.Column(db.Float, nullable=False)
    mention = db.Column(db.String, nullable=False)
    reussi = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        """Sérialise l'évaluation pour une réponse JSON."""
        return {
            "id": self.id,
            "notes": [float(x) for x in self.notes.split(",")],
            "moyenne": self.moyenne,
            "mention": self.mention,
            "reussi": self.reussi,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
