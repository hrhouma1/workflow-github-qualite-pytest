"""Logique métier du projet : validation, moyenne, mention et réussite.

Ce module est volontairement simple afin de servir de support pédagogique
pour illustrer les tests unitaires (pytest) et l'intégration continue (CI).
"""


def valider_note(note: float) -> None:
    """Vérifie qu'une note est un nombre compris entre 0 et 100.

    Args:
        note: La note à valider.

    Raises:
        TypeError: Si la note n'est pas un nombre.
        ValueError: Si la note est en dehors de l'intervalle [0, 100].
    """
    # On exclut explicitement les booléens : en Python, bool est une
    # sous-classe de int, donc True passerait sinon pour la valeur 1.
    if isinstance(note, bool) or not isinstance(note, (int, float)):
        raise TypeError("La note doit être un nombre.")

    if note < 0 or note > 100:
        raise ValueError("La note doit être comprise entre 0 et 100.")


def calculer_moyenne(notes: list[float]) -> float:
    """Calcule la moyenne arrondie d'une liste de notes.

    Args:
        notes: Liste de notes valides.

    Returns:
        La moyenne arrondie à deux décimales.

    Raises:
        ValueError: Si la liste est vide.
        TypeError: Si une note n'est pas un nombre.
    """
    if len(notes) == 0:
        raise ValueError("La liste des notes ne peut pas être vide.")

    for note in notes:
        valider_note(note)

    return round(sum(notes) / len(notes), 2)


def determiner_mention(moyenne: float) -> str:
    """Retourne la mention associée à une moyenne.

    Args:
        moyenne: La moyenne à évaluer.

    Returns:
        Une mention textuelle ("Excellent", "Très bien", ...).
    """
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
    """Indique si une moyenne correspond à une réussite (>= 60).

    Args:
        moyenne: La moyenne à évaluer.

    Returns:
        True si la moyenne est supérieure ou égale à 60, sinon False.
    """
    valider_note(moyenne)
    return moyenne >= 60
