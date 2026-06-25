"""Schémas Pydantic (validation des entrées / sérialisation des sorties)."""

from datetime import datetime

from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    """Données attendues pour créer une évaluation."""

    notes: list[float] = Field(..., min_length=1, examples=[[80, 90, 100]])


class EvaluationRead(BaseModel):
    """Représentation renvoyée par l'API pour une évaluation."""

    id: int
    notes: list[float]
    moyenne: float
    mention: str
    reussi: bool
    created_at: datetime
