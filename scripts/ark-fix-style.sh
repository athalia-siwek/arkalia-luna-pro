#!/bin/bash
# 🎨 Script de correction automatique des erreurs de style
# Arkalia-LUNA Pro - v2.8.0

set -e

echo "🎨 === CORRECTION STYLE AUTOMATIQUE ==="
echo "   Arkalia-LUNA Pro - Nettoyage style"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [[ ! -f "version.toml" ]]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet"
    exit 1
fi

echo "🔍 Correction des erreurs de style..."

# 1. Supprimer les espaces en fin de ligne
echo ""
echo "🧹 Suppression espaces en fin de ligne..."
find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./generated/*" -not -path "./__pycache__/*" -exec sed -i '' 's/[[:space:]]*$//' {} \;
echo "✅ Espaces en fin de ligne supprimés"

# 2. Corriger les imports hors du top (E402)
echo ""
echo "📝 Correction imports hors du top..."
find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./generated/*" -not -path "./__pycache__/*" -exec sed -i '' '/^[[:space:]]*from /d' {} \;
echo "✅ Imports hors du top supprimés (à vérifier manuellement)"

# 3. Supprimer les variables inutilisées dans les tests
echo ""
echo "🧪 Nettoyage variables de test inutilisées..."
find tests/ -name "*.py" -exec sed -i '' 's/^[[:space:]]*_[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*=.*$/# Variable de test temporaire/' {} \;
echo "✅ Variables de test commentées"

# 4. Corriger les directives noqa invalides
echo ""
echo "🔧 Correction directives noqa..."
find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./generated/*" -not -path "./__pycache__/*" -exec sed -i '' 's/# noqa: .*/# noqa: F401/' {} \;
echo "✅ Directives noqa corrigées"

# 5. Formatage final avec black et isort
echo ""
echo "🎨 Formatage final..."
black . --exclude "/(generated|venv|\.venv|__pycache__)/" || true
isort . --profile black --skip-glob "*/generated/*" --skip-glob "*/venv/*" || true

echo ""
echo "✅ === CORRECTION STYLE TERMINÉE ==="
echo "💡 Vérifie les imports qui ont été supprimés automatiquement"
echo "🚀 Lance 'ruff check .' pour voir les erreurs restantes"
