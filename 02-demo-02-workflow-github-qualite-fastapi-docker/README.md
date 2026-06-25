# Démo 02 — CI/CD avec FastAPI, PostgreSQL et Docker Compose

> Niveau 2 de la progression « Automatiser la qualité logicielle ».
> On passe d'une simple fonction testée (démo 01) à une **vraie application
> multi-services** (API + base de données) construite et vérifiée automatiquement.

Cette API expose la logique des notes (moyenne, mention, réussite) via HTTP et
**historise chaque évaluation** dans une base **PostgreSQL**. Le tout est
orchestré par **Docker Compose** et validé par un pipeline **CI/CD GitHub Actions**.

---

## 1. Ce que ce projet ajoute par rapport à la démo 01

| Démo 01 (bases) | Démo 02 (ce projet) |
|---|---|
| Une fonction Python | Une **API HTTP** (FastAPI) |
| Tests unitaires | Tests unitaires **+ tests d'intégration de l'API** |
| Pas de base de données | **PostgreSQL** pour persister les évaluations |
| Pas de conteneur | **Dockerfile + docker-compose** (2 services) |
| CI (tests) | **CI/CD** : tests + build d'image + exécution réelle des conteneurs |

---

## 2. Structure du projet

```text
02-demo-02-.../
├── app/
│   ├── __init__.py
│   ├── notes.py          # Logique métier (réutilisée de la démo 01)
│   ├── database.py       # Connexion SQLAlchemy (DATABASE_URL)
│   ├── models.py         # Table "evaluations"
│   ├── schemas.py        # Schémas Pydantic (entrées/sorties)
│   └── main.py           # API FastAPI (routes)
├── tests/
│   ├── conftest.py       # Base SQLite isolée pour les tests
│   ├── test_notes.py     # Tests unitaires
│   └── test_api.py       # Tests d'intégration de l'API
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

Documentation interactive auto-générée : **http://localhost:8000/docs** (Swagger UI).

---

## 4. Lancer le projet avec Docker Compose (recommandé)

```bash
# (optionnel) créer le fichier .env à partir de l'exemple
cp .env.example .env

# construire et démarrer l'API + PostgreSQL
docker compose up --build
```

Puis testez :

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/evaluations \
  -H "Content-Type: application/json" \
  -d '{"notes": [80, 90, 100]}'

curl http://localhost:8000/evaluations
```

Pour tout arrêter et supprimer le volume de la base :

```bash
docker compose down -v
```

---

## 5. Développement / tests en local (sans Docker)

Les tests utilisent **SQLite en mémoire** : aucune base PostgreSQL n'est requise.

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

ruff check app tests
pytest --cov=app --cov-report=term-missing
```

### macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ruff check app tests
pytest --cov=app --cov-report=term-missing
```

Pour lancer l'API en local sans Docker (nécessite un PostgreSQL accessible
via `DATABASE_URL`, ou adaptez l'URL) :

```bash
uvicorn app.main:app --reload
```

---

## 6. Le pipeline CI/CD (`.github/workflows/ci.yml`)

Le workflow comporte **deux jobs** :

1. **`tests`** — installe Python, vérifie le style (Ruff), lance les tests avec
   couverture (`pytest-cov`) et publie le rapport HTML en artefact.
2. **`docker`** — (après le succès des tests) construit l'image, démarre
   `api + postgres` via `docker compose`, attend que `/health` réponde,
   teste un appel réel `POST /evaluations`, puis nettoie les conteneurs.

C'est la différence clé entre **CI** (on teste le code) et **CD** : ici on
**construit et exécute réellement l'application conteneurisée** pour prouver
qu'elle démarre et fonctionne de bout en bout.

---

## 7. Idées d'exercices pour la classe

- Ajouter un endpoint `DELETE /evaluations/{id}` + son test.
- Ajouter une colonne `etudiant` (nom) et l'exposer dans l'API.
- Casser volontairement la logique (`>=` en `>`) et observer la CI passer au rouge.
- Ajouter un second service (ex : pgAdmin) dans `docker-compose.yml`.

---

## 8. Badge de statut (optionnel)

```markdown
![CI/CD](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)
```
