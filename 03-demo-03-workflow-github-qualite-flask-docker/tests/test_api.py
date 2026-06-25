"""Tests d'intégration de l'API Flask (via la base SQLite de test)."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_creer_evaluation(client):
    response = client.post("/evaluations", json={"notes": [80, 90, 100]})
    assert response.status_code == 201
    data = response.get_json()
    assert data["moyenne"] == 90.0
    assert data["mention"] == "Excellent"
    assert data["reussi"] is True
    assert data["notes"] == [80.0, 90.0, 100.0]
    assert data["id"] >= 1


def test_creer_evaluation_echec(client):
    response = client.post("/evaluations", json={"notes": [40, 50]})
    assert response.status_code == 201
    data = response.get_json()
    assert data["mention"] == "Échec"
    assert data["reussi"] is False


def test_creer_evaluation_note_invalide(client):
    response = client.post("/evaluations", json={"notes": [120]})
    assert response.status_code == 422


def test_creer_evaluation_notes_absentes(client):
    response = client.post("/evaluations", json={})
    assert response.status_code == 422


def test_lister_evaluations(client):
    client.post("/evaluations", json={"notes": [60, 60]})
    client.post("/evaluations", json={"notes": [100]})
    response = client.get("/evaluations")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_obtenir_evaluation(client):
    cree = client.post("/evaluations", json={"notes": [70, 80]}).get_json()
    response = client.get(f"/evaluations/{cree['id']}")
    assert response.status_code == 200
    assert response.get_json()["id"] == cree["id"]


def test_obtenir_evaluation_introuvable(client):
    response = client.get("/evaluations/999")
    assert response.status_code == 404
