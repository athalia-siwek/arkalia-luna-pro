FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du module
COPY modules/error_recovery /app/modules/error_recovery

# Port pour l'API
EXPOSE 8017

# Commande de démarrage
CMD ["python", "-m", "modules.error_recovery.core"]
