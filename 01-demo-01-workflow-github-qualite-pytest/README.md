# Automatiser la qualité logicielle avec GitHub Actions, Pytest et la CI/CD

> De la fonction Python au workflow GitHub : tester, valider et sécuriser chaque modification de code.

Ce projet pédagogique montre **de A à Z** comment utiliser les **workflows GitHub Actions**
pour garantir la **qualité d'un projet Python**, à l'aide de `pytest`, `pytest-cov` et `ruff`.

L'application est volontairement minimale : elle calcule la **moyenne** d'une liste de notes,
la **mention** associée, la **réussite/échec**, et lève des **erreurs** si les notes sont invalides.

---

## 1. Objectif pédagogique

| Notion | Ce que l'apprenant comprend |
|---|---|
| **Test unitaire** | Une petite fonction peut être vérifiée automatiquement |
| **pytest** | Les tests sont écrits dans des fichiers `test_*.py` |
| **CI** | Le code est testé automatiquement après chaque `push` |
| **GitHub Actions** | GitHub exécute des étapes définies dans un fichier YAML |
| **Pull Request** | On peut vérifier le code avant de le fusionner |
| **Couverture** | On mesure les parties du code couvertes par les tests |
| **Qualité logicielle** | On évite de livrer du code cassé |
| **Automatisation** | La vérification ne dépend plus seulement de l'humain |

---

## 2. Structure du projet

```text
ci-quality-python/
│
├── app/
│   ├── __init__.py
│   └── notes.py            # Logique métier (moyenne, mention, réussite)
│
├── tests/
│   └── test_notes.py       # Tests unitaires pytest
│
├── .github/
│   └── workflows/
│       ├── ci.yml          # Workflow CI principal (Python 3.12 + couverture)
│       └── ci-matrix.yml   # Variante multi-versions (3.10, 3.11, 3.12)
│
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## 3. Installation locale

### Sur Windows (PowerShell)

```powershell
# Créer l'environnement virtuel avec Python 3.12
py -3.12 -m venv .venv
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Sur macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Commandes utiles

| Action | Commande |
|---|---|
| Lancer les tests | `pytest` |
| Tests + couverture (terminal) | `pytest --cov=app --cov-report=term-missing` |
| Tests + couverture (rapport HTML) | `pytest --cov=app --cov-report=html` |
| Vérifier le style du code | `ruff check app tests` |
| Corriger automatiquement le style | `ruff check --fix app tests` |

Le rapport HTML est généré dans le dossier `htmlcov/` : ouvrez `htmlcov/index.html` dans un navigateur.

**Résultat attendu des tests :**

```text
13 passed
```

---

## 5. Le workflow GitHub Actions (`.github/workflows/ci.yml`)

Le workflow se déclenche automatiquement :

- à chaque `push` sur la branche `main` ;
- à chaque **pull request** vers `main`.

Étapes exécutées par GitHub :

1. Récupérer le code (`actions/checkout`)
2. Installer Python 3.12 (`actions/setup-python`)
3. Installer les dépendances (`pip install -r requirements.txt`)
4. Vérifier le style avec **Ruff**
5. Exécuter les **tests** avec **Pytest**
6. Calculer la **couverture** avec **pytest-cov**
7. Sauvegarder le rapport HTML comme **artefact** téléchargeable

Le statut (vert ✅ / rouge ❌) s'affiche dans l'onglet **Actions** et sur chaque commit / pull request.

---

## 6. Scénario pédagogique en classe

### Étape 1 — Exécuter les tests localement

```bash
pytest
```

Objectif : comprendre qu'un test vérifie automatiquement que le code fonctionne.

### Étape 2 — Créer un dépôt GitHub

```bash
git init
git add .
git commit -m "Initialisation du projet avec tests pytest"
git branch -M main
git remote add origin https://github.com/USERNAME/ci-quality-python.git
git push -u origin main
```

> Remplacez `USERNAME` par votre compte GitHub réel.

### Étape 3 — Observer GitHub Actions

Après le `git push`, GitHub détecte automatiquement `.github/workflows/ci.yml`.
Dans l'onglet **Actions**, les apprenants voient le workflow s'exécuter en direct.

### Étape 4 — Provoquer volontairement une erreur

Dans `app/notes.py`, remplacez temporairement :

```python
return moyenne >= 60
```

par :

```python
return moyenne > 60
```

Puis :

```bash
git add .
git commit -m "Introduire une erreur volontaire"
git push
```

Le test suivant va **échouer** :

```python
def test_reussite_true():
    assert est_reussi(60) is True
```

Objectif : montrer que GitHub Actions **bloque automatiquement** une erreur logique. ❌

### Étape 5 — Corriger l'erreur

Remettez `return moyenne >= 60`, puis :

```bash
git add .
git commit -m "Corriger la logique de réussite"
git push
```

Le workflow redevient **vert**. ✅

---

## 7. Variante avancée : tester plusieurs versions de Python

Le fichier `.github/workflows/ci-matrix.yml` utilise une **matrice** pour exécuter
les tests sur plusieurs versions de Python en parallèle :

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

Cela permet de garantir que le code fonctionne sur toutes les versions ciblées.

---

## 8. Badge de statut (optionnel)

Ajoutez un badge en haut de ce README pour afficher l'état du workflow
(remplacez `USERNAME` et `ci-quality-python`) :

```markdown
![CI](https://github.com/USERNAME/ci-quality-python/actions/workflows/ci.yml/badge.svg)
```
