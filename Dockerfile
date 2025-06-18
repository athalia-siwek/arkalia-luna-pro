# 🐍 Base légère Python 3.10
FROM python:3.10-slim

# 📁 Dossier de travail dans le conteneur
WORKDIR /app

# 🧠 Copie du code source dans l'image
COPY . /app

# 📦 Installation des dépendances
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 🌐 Port exposé pour Uvicorn
EXPOSE 8000

# 🚀 Lancement avec rechargement intelligent
CMD ["uvicorn", "helloria.core:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "helloria", "--reload-exclude", "logs/", "--reload-exclude", "docs/", "--reload-exclude", "site/"]