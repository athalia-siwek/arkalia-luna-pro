# 🚀 Dockerfile Arkalia-LUNA Optimisé - Multi-stage Build
# Stage 1: Builder - Installation des dépendances
FROM python:3.10-slim AS builder

# Variables d'optimisation
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Installation des outils de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Création d'un environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copie et installation des dépendances
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Image finale légère
FROM python:3.10-slim AS runtime

# Métadonnées
LABEL maintainer="Athalia <athalia@arkalia.ai>"
LABEL description="Arkalia-LUNA API Core"
LABEL version="3.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"

# Installation des outils système
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Création utilisateur non-root
RUN groupadd -r arkalia && \
    useradd -r -g arkalia -d /app -s /bin/bash arkalia && \
    mkdir -p /app/logs /app/state && \
    chown -R arkalia:arkalia /app

# Copie du venv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Répertoire de travail
WORKDIR /app

# Copie du code avec permissions correctes
COPY --chown=arkalia:arkalia helloria ./helloria
COPY --chown=arkalia:arkalia modules ./modules
COPY --chown=arkalia:arkalia state ./state
COPY --chown=arkalia:arkalia config ./config
COPY --chown=arkalia:arkalia run_arkalia_api.py ./

# Switch vers utilisateur non-root
USER arkalia

# Port exposé
EXPOSE 8000

# Point d'entrée optimisé avec script de démarrage robuste
CMD ["python", "run_arkalia_api.py"]
