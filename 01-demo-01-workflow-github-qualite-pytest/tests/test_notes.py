"""Tests unitaires des fonctions du module app.notes."""

import pytest

from app.notes import calculer_moyenne, determiner_mention, est_reussi, valider_note


def test_calculer_moyenne_valide():
    resultat = calculer_moyenne([80, 90, 100])
    assert resultat == 90.0


def test_calculer_moyenne_avec_decimales():
    resultat = calculer_moyenne([75.5, 80.5, 84])
    assert resultat == 80.0


def test_calculer_moyenne_liste_vide():
    with pytest.raises(ValueError):
        calculer_moyenne([])


def test_note_negative_invalide():
    with pytest.raises(ValueError):
        valider_note(-5)


def test_note_superieure_a_100_invalide():
    with pytest.raises(ValueError):
        valider_note(120)


def test_note_non_numerique_invalide():
    with pytest.raises(TypeError):
        valider_note("90")


def test_mention_excellent():
    assert determiner_mention(95) == "Excellent"


def test_mention_tres_bien():
    assert determiner_mention(85) == "Très bien"


def test_mention_bien():
    assert determiner_mention(75) == "Bien"


def test_mention_passable():
    assert determiner_mention(65) == "Passable"


def test_mention_echec():
    assert determiner_mention(45) == "Échec"


def test_reussite_true():
    assert est_reussi(60) is True


def test_reussite_false():
    assert est_reussi(59.99) is False
