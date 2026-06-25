"""Modèles ORM (tables SQLAlchemy)."""

from sqlalchemy import Boolean, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Evaluation(Base):
    """Une évaluation persistée : les notes saisies et leur résultat calculé."""

    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Les notes sont stockées en CSV pour rester simple (ex : "80,90,100").
    notes: Mapped[str] = mapped_column(String, nullable=False)
    moyenne: Mapped[float] = mapped_column(Float, nullable=False)
    mention: Mapped[str] = mapped_column(String, nullable=False)
    reussi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
