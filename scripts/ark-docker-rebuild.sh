#!/bin/bash
# 🔁 Rebuild et relance propre de l’environnement Docker d’Arkalia

echo "🧼 Nettoyage des fichiers parasites..."
find . -name '._*' -delete
find . -name '.DS_Store' -delete

echo "🧹 Docker cleanup..."
docker-compose down

echo "🛠 Rebuild complet de l'image Docker..."
docker-compose build --no-cache

echo "🚀 Démarrage du conteneur..."
docker-compose up