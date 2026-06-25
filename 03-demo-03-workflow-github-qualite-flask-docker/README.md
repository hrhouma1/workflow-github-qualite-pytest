# Démo 03 — CI/CD avec Flask, PostgreSQL et Docker Compose

> Même objectif que la démo 02, mais avec **Flask** (au lieu de FastAPI).
> Idéal pour comparer deux frameworks sur un cas identique : API qui calcule
> moyenne / mention / réussite et historise les évaluations dans PostgreSQL.

---

## 1. FastAPI (démo 02) vs Flask (démo 03)

| Aspect | FastAPI (démo 02) | Flask (démo 03) |
|---|---|---|
| Style | Asynchrone, typage Pydantic | Synchrone, minimaliste |
| Validation | Schémas Pydantic automatiques | Validation manuelle dans la route |
| Doc auto | Swagger `/docs` intégré | Aucune par défaut |
| ORM | SQLAlchemy "pur" | Flask-SQLAlchemy |
| Serveur prod | `uvicorn` (ASGI) | `gunicorn` (WSGI) |
| Patron | Module `app` global | **Application factory** `create_app()` |

L'API et la base de données sont **identiques** : seul le framework change.

---

## 2. Structure du projet

```text
03-demo-03-.../
├── app/
│   ├── __init__.py       # Factory create_app()
│   ├── extensions.py     # Instance SQLAlchemy partagée
│   ├── notes.py          # Logique métier (réutilisée)
│   ├── models.py         # Table "evaluations"
│   └── routes.py         # Blueprint avec les endpoints
├── tests/
│   ├── conftest.py       # App Flask sur SQLite isolée
│   ├── test_notes.py     # Tests unitaires
│   └── test_api.py       # Tests d'intégration de l'API
├── wsgi.py               # Point d'entrée gunicorn
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 3. Les endpoints de l'API

| Méthode | Chemin | Description |
|---|---|---|
| `GET` | `/health` | Vérifie que l'API est vivante |
| `POST` | `/evaluations` | Calcule + enregistre une évaluation (`{"notes": [80, 90]}`) |
| `GET` | `/evaluations` | Liste toutes les évaluations |
| `GET` | `/evaluations/{id}` | Récupère une évaluation par son id |

---

## 4. Lancer le projet avec Docker Compose (recommandé)

```bash
cp .env.example .env          # optionnel
docker compose up --build
```

Tester :

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/evaluations \
  -H "Content-Type: application/json" \
  -d '{"notes": [80, 90, 100]}'

curl http://localhost:8000/evaluations
```

Arrêter :

```bash
docker compose down -v
```

---

## 5. Développement / tests en local (sans Docker)

Les tests utilisent **SQLite en mémoire** : aucun PostgreSQL requis.

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

ruff check app tests wsgi.py
pytest --cov=app --cov-report=term-missing
```

### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ruff check app tests wsgi.py
pytest --cov=app --cov-report=term-missing
```

Lancer l'API en local (serveur de dev Flask) :

```bash
flask --app wsgi run --debug
```

---

## 6. Le pipeline CI/CD (`.github/workflows/ci.yml`)

Deux jobs, comme la démo 02 :

1. **`tests`** — Ruff + `pytest` avec couverture (rapport HTML en artefact).
2. **`docker`** — `docker compose up --build`, attente de `/health`, appel réel
   `POST /evaluations`, puis nettoyage. On prouve que l'app **conteneurisée**
   démarre et fonctionne de bout en bout.

---

## 7. Idées d'exercices pour la classe

- Ajouter une validation plus stricte (ex : refuser plus de 50 notes).
- Ajouter `DELETE /evaluations/{id}` + test.
- Comparer le code Flask et FastAPI : lequel est le plus lisible pour vous ?
- Casser volontairement la logique et observer la CI passer au rouge.

---

## 8. Badge de statut (optionnel)

```markdown
![CI/CD](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)
```
