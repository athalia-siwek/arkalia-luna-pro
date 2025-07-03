#!/bin/bash
set -e

# Dossier de sortie pour les rapports
REPORTS_DIR="tests/reports"
mkdir -p "$REPORTS_DIR"

# Nettoyage des anciens rapports
rm -rf htmlcov/ "$REPORTS_DIR"/*

# Exécution des tests unitaires avec couverture
pytest --cov=modules --cov-report=html --cov-report=term-missing tests/unit

# Exécution des tests d'intégration
pytest -c pytest-integration.ini tests/integration

# --- Démarrage de l'API pour les tests E2E ---
echo "\n🚀 Démarrage de l'API (FastAPI) via Docker Compose..."
docker-compose up -d arkalia-api

# Attente de disponibilité de l'API
API_URL="http://localhost:8000/reason"
for i in {1..10}; do
  if curl -s -o /dev/null -w "%{http_code}" "$API_URL" | grep -q "[24][0-9][0-9]"; then
    echo "✅ API disponible sur $API_URL"
    break
  fi
  echo "⏳ Attente de l'API ($i/10)..."
  sleep 2
done

# Exécution des tests E2E
pytest tests/e2e

# Arrêt de l'API (optionnel)
echo "⏹️ Arrêt de l'API (FastAPI)"
docker-compose stop arkalia-api

# Exécution des tests de chaos
pytest tests/chaos

# Exécution des tests de performance
pytest tests/performance

# Exécution des tests de sécurité
pytest tests/security

# Déplacement des rapports de couverture HTML
if [ -d htmlcov ]; then
  mv htmlcov "$REPORTS_DIR/htmlcov"
fi

# Déplacement d'autres rapports (benchmarks, logs, etc.) si besoin
# Exemple : mv benchmark_results "$REPORTS_DIR/" 2>/dev/null || true

# Résumé
pytest --maxfail=1 --disable-warnings -v --collect-only | tee "$REPORTS_DIR/pytest_collection.txt"
echo "\n🌕 Tous les tests sont terminés. Les rapports sont dans $REPORTS_DIR/"
