"""Routes de l'API (blueprint Flask)."""

from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Evaluation
from app.notes import calculer_moyenne, determiner_mention, est_reussi

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    """Point de santé utilisé par Docker Compose et la CI."""
    return {"status": "ok"}


@bp.post("/evaluations")
def creer_evaluation():
    """Calcule le résultat d'une liste de notes et l'enregistre en base."""
    data = request.get_json(silent=True) or {}
    notes = data.get("notes")

    if not isinstance(notes, list):
        return {"detail": "Le champ 'notes' doit être une liste non vide."}, 422

    try:
        moyenne = calculer_moyenne(notes)
    except (ValueError, TypeError) as exc:
        return {"detail": str(exc)}, 422

    evaluation = Evaluation(
        notes=",".join(str(note) for note in notes),
        moyenne=moyenne,
        mention=determiner_mention(moyenne),
        reussi=est_reussi(moyenne),
    )
    db.session.add(evaluation)
    db.session.commit()
    return jsonify(evaluation.to_dict()), 201


@bp.get("/evaluations")
def lister_evaluations():
    """Renvoie toutes les évaluations enregistrées."""
    evaluations = Evaluation.query.order_by(Evaluation.id).all()
    return jsonify([evaluation.to_dict() for evaluation in evaluations])


@bp.get("/evaluations/<int:evaluation_id>")
def obtenir_evaluation(evaluation_id: int):
    """Renvoie une évaluation par son identifiant."""
    evaluation = db.session.get(Evaluation, evaluation_id)
    if evaluation is None:
        return {"detail": "Évaluation introuvable."}, 404
    return jsonify(evaluation.to_dict())
