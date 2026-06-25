# Image légère officielle Python
FROM python:3.12-slim

# Évite les .pyc et force des logs non bufferisés (utile dans les conteneurs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) On copie d'abord les dépendances pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Puis le code de l'application
COPY . .

EXPOSE 8000

# Démarrage du serveur ASGI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
