#!/bin/bash
# 🔁 Arkalia - Push Final Automatisé
# Version : v2.5.0+

echo "🔁 Push final en cours..."
echo "🔧 Formatage + linting"
ark-fixall

echo "🧪 Tests & coverage"
pytest --cov=modules/ --cov-report=term-missing

echo "💾 Ajout des fichiers"
git add .

echo "✍️ Commit"
git commit -m "push: version stable validée"

echo "🏷️ Tag Git auto"
DATE_TAG=$(date "+%Y-%m-%d_%Hh%Mm")
git tag "push-${DATE_TAG}"

echo "🚀 Push"
git push && git push --tags

echo "📡 Déploiement mkdocs"
ark-docs

echo "✅ Terminé. CI/CD local complet exécuté."
