"""Tests d'intégration de l'API (via la base SQLite de test)."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_creer_evaluation(client):
    response = client.post("/evaluations", json={"notes": [80, 90, 100]})
    assert response.status_code == 201
    data = response.json()
    assert data["moyenne"] == 90.0
    assert data["mention"] == "Excellent"
    assert data["reussi"] is True
    assert data["notes"] == [80.0, 90.0, 100.0]
    assert data["id"] >= 1


def test_creer_evaluation_echec(client):
    response = client.post("/evaluations", json={"notes": [40, 50]})
    assert response.status_code == 201
    data = response.json()
    assert data["mention"] == "Échec"
    assert data["reussi"] is False


def test_creer_evaluation_note_invalide(client):
    response = client.post("/evaluations", json={"notes": [120]})
    assert response.status_code == 422


def test_creer_evaluation_liste_vide(client):
    # min_length=1 dans le schéma Pydantic -> rejet avant la logique métier.
    response = client.post("/evaluations", json={"notes": []})
    assert response.status_code == 422


def test_lister_evaluations(client):
    client.post("/evaluations", json={"notes": [60, 60]})
    client.post("/evaluations", json={"notes": [100]})
    response = client.get("/evaluations")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obtenir_evaluation(client):
    cree = client.post("/evaluations", json={"notes": [70, 80]}).json()
    response = client.get(f"/evaluations/{cree['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == cree["id"]


def test_obtenir_evaluation_introuvable(client):
    response = client.get("/evaluations/999")
    assert response.status_code == 404
