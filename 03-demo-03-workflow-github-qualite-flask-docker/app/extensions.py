"""Extensions Flask partagées.

`db` est défini ici (sans application) puis relié à l'app via `db.init_app`
dans la factory. Cela évite les imports circulaires entre modèles et app.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
