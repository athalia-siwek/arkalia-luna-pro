FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie sélective du code
COPY --chown=cognitive:cognitive modules/cognitive_reactor ./modules/cognitive_reactor
COPY --chown=cognitive:cognitive modules/monitoring ./modules/monitoring
COPY --chown=cognitive:cognitive modules/utils_enhanced ./modules/utils_enhanced
COPY --chown=cognitive:cognitive modules/__init__.py ./modules/
COPY --chown=cognitive:cognitive config ./config
COPY --chown=cognitive:cognitive state ./state

# Port pour l'API
EXPOSE 8015

# Commande de démarrage
CMD ["python", "-m", "modules.cognitive_reactor.core"]
