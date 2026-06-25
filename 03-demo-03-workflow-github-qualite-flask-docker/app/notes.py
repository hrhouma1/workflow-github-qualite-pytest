"""Logique métier : validation, moyenne, mention et réussite.

Identique aux démos 01 et 02 : c'est le coeur testable, ici réutilisé
derrière une API Flask.
"""


def valider_note(note: float) -> None:
    """Vérifie qu'une note est un nombre compris entre 0 et 100."""
    if isinstance(note, bool) or not isinstance(note, (int, float)):
        raise TypeError("La note doit être un nombre.")

    if note < 0 or note > 100:
        raise ValueError("La note doit être comprise entre 0 et 100.")


def calculer_moyenne(notes: list[float]) -> float:
    """Calcule la moyenne arrondie (2 décimales) d'une liste de notes."""
    if len(notes) == 0:
        raise ValueError("La liste des notes ne peut pas être vide.")

    for note in notes:
        valider_note(note)

    return round(sum(notes) / len(notes), 2)


def determiner_mention(moyenne: float) -> str:
    """Retourne la mention associée à une moyenne."""
    valider_note(moyenne)

    if moyenne >= 90:
        return "Excellent"
    elif moyenne >= 80:
        return "Très bien"
    elif moyenne >= 70:
        return "Bien"
    elif moyenne >= 60:
        return "Passable"
    else:
        return "Échec"


def est_reussi(moyenne: float) -> bool:
    """Indique si une moyenne correspond à une réussite (>= 60)."""
    valider_note(moyenne)
    return moyenne >= 60
