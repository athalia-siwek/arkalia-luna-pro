FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du module
COPY modules/crossmodule_validator /app/modules/crossmodule_validator

# Port pour l'API
EXPOSE 8016

# Commande de démarrage
CMD ["python", "-m", "modules.crossmodule_validator.core"] 