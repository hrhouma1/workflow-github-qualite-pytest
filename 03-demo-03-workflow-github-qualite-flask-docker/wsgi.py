"""Point d'entrée WSGI pour le serveur de production (gunicorn).

Utilisé par le conteneur Docker :  gunicorn --bind 0.0.0.0:8000 wsgi:app
"""

from app import create_app

app = create_app()
