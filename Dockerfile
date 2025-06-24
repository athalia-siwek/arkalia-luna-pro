# 🐍 Base légère Python 3.10
FROM python:3.10-slim

# 📁 Dossier de travail dans le conteneur
WORKDIR /app

# 📦 Pré-copie requirements.txt pour cache Docker optimisé
COPY requirements.txt .

# 🔁 Installation des dépendances sans cache
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 🧠 Copie du code source
COPY helloria /app/helloria
COPY modules /app/modules
COPY state /app/state
COPY config /app/config

# 🌐 Port exposé pour Uvicorn
EXPOSE 8000

# 🚀 Lancement du serveur API Helloria
CMD ["uvicorn", "helloria.core:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "helloria", "--reload-exclude", "logs/", "--reload-exclude", "docs/", "--reload-exclude", "site/"]
