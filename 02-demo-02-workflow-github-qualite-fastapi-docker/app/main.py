"""Application FastAPI : expose la logique des notes via une API HTTP."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db
from app.notes import calculer_moyenne, determiner_mention, est_reussi


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Crée les tables au démarrage (quand une vraie base est disponible)."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Qualité des Notes",
    description="Calcule moyenne, mention et réussite, et historise les évaluations.",
    version="1.0.0",
    lifespan=lifespan,
)


def _to_read(evaluation: models.Evaluation) -> schemas.EvaluationRead:
    """Convertit un enregistrement ORM en schéma de sortie."""
    return schemas.EvaluationRead(
        id=evaluation.id,
        notes=[float(x) for x in evaluation.notes.split(",")],
        moyenne=evaluation.moyenne,
        mention=evaluation.mention,
        reussi=evaluation.reussi,
        created_at=evaluation.created_at,
    )


@app.get("/health", tags=["système"])
def health() -> dict:
    """Point de santé utilisé par Docker Compose et la CI."""
    return {"status": "ok"}


@app.post(
    "/evaluations",
    response_model=schemas.EvaluationRead,
    status_code=201,
    tags=["évaluations"],
)
def creer_evaluation(
    payload: schemas.EvaluationCreate, db: Session = Depends(get_db)
) -> schemas.EvaluationRead:
    """Calcule le résultat d'une liste de notes et l'enregistre en base."""
    try:
        moyenne = calculer_moyenne(payload.notes)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    evaluation = models.Evaluation(
        notes=",".join(str(note) for note in payload.notes),
        moyenne=moyenne,
        mention=determiner_mention(moyenne),
        reussi=est_reussi(moyenne),
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return _to_read(evaluation)


@app.get(
    "/evaluations",
    response_model=list[schemas.EvaluationRead],
    tags=["évaluations"],
)
def lister_evaluations(db: Session = Depends(get_db)) -> list[schemas.EvaluationRead]:
    """Renvoie toutes les évaluations enregistrées."""
    evaluations = db.query(models.Evaluation).order_by(models.Evaluation.id).all()
    return [_to_read(evaluation) for evaluation in evaluations]


@app.get(
    "/evaluations/{evaluation_id}",
    response_model=schemas.EvaluationRead,
    tags=["évaluations"],
)
def obtenir_evaluation(
    evaluation_id: int, db: Session = Depends(get_db)
) -> schemas.EvaluationRead:
    """Renvoie une évaluation par son identifiant."""
    evaluation = db.get(models.Evaluation, evaluation_id)
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Évaluation introuvable.")
    return _to_read(evaluation)
