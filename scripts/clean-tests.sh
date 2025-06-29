#!/bin/bash
# 🧹 Script de nettoyage automatique pour les tests Arkalia-LUNA

set -e

echo "🧹 Nettoyage automatique des tests Arkalia-LUNA..."

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier qu'on est dans le bon répertoire
if [[ ! -f "version.toml" ]]; then
    log_error "Ce script doit être exécuté depuis la racine du projet Arkalia-LUNA"
    exit 1
fi

log_info "Début du nettoyage..."

# 1. Nettoyer les fichiers Python compilés
log_info "Nettoyage des fichiers Python compilés..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
log_success "Fichiers Python compilés supprimés"

# 2. Nettoyer les rapports de couverture
log_info "Nettoyage des rapports de couverture..."
rm -rf htmlcov/ 2>/dev/null || true
rm -rf .coverage 2>/dev/null || true
rm -rf coverage.xml 2>/dev/null || true
log_success "Rapports de couverture supprimés"

# 3. Nettoyer le cache pytest
log_info "Nettoyage du cache pytest..."
rm -rf .pytest_cache/ 2>/dev/null || true
rm -rf .cache/ 2>/dev/null || true
log_success "Cache pytest supprimé"

# 4. Nettoyer les fichiers temporaires de test
log_info "Nettoyage des fichiers temporaires de test..."
find . -name "test_*.tmp" -delete 2>/dev/null || true
find . -name "temp_*" -type f -delete 2>/dev/null || true
find . -name "*.backup" -delete 2>/dev/null || true
log_success "Fichiers temporaires supprimés"

# 5. Nettoyer les fichiers d'état de test
log_info "Nettoyage des fichiers d'état de test..."
find . -name "test_*.toml" -delete 2>/dev/null || true
find . -name "test_*.json" -delete 2>/dev/null || true
find . -name "test_*.db" -delete 2>/dev/null || true
log_success "Fichiers d'état de test supprimés"

# 6. Nettoyer les artefacts de benchmark
log_info "Nettoyage des artefacts de benchmark..."
rm -rf benchmark_results/ 2>/dev/null || true
find . -name "*.bench" -delete 2>/dev/null || true
log_success "Artefacts de benchmark supprimés"

# 7. Nettoyer les logs de test
log_info "Nettoyage des logs de test..."
find . -name "test_*.log" -delete 2>/dev/null || true
find . -name "pytest_*.log" -delete 2>/dev/null || true
log_success "Logs de test supprimés"

# 8. Nettoyer les fichiers de rapport
log_info "Nettoyage des fichiers de rapport..."
find . -name "test-results.xml" -delete 2>/dev/null || true
find . -name "junit.xml" -delete 2>/dev/null || true
find . -name "coverage.xml" -delete 2>/dev/null || true
log_success "Fichiers de rapport supprimés"

# 9. Nettoyer les répertoires temporaires de test
log_info "Nettoyage des répertoires temporaires..."
find . -name "test_*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "temp_*" -type d -exec rm -rf {} + 2>/dev/null || true
log_success "Répertoires temporaires supprimés"

# 10. Nettoyer les fichiers macOS
log_info "Nettoyage des fichiers macOS..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "._*" -delete 2>/dev/null || true
log_success "Fichiers macOS supprimés"

# 11. Nettoyer les fichiers de lock
log_info "Nettoyage des fichiers de lock..."
find . -name "*.lock" -delete 2>/dev/null || true
log_success "Fichiers de lock supprimés"

# 12. Vérifier l'espace disque libéré
log_info "Calcul de l'espace libéré..."
BEFORE=$(df . | awk 'NR==2 {print $3}')
# Le nettoyage a déjà été fait, on calcule juste pour l'affichage
AFTER=$(df . | awk 'NR==2 {print $3}')
FREED=$((BEFORE - AFTER))
log_success "Nettoyage terminé"

# 13. Afficher le résumé
echo ""
echo "📊 Résumé du nettoyage :"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_success "✅ Nettoyage complet terminé"
echo "📁 Répertoires nettoyés :"
echo "   • __pycache__"
echo "   • .pytest_cache"
echo "   • htmlcov"
echo "   • benchmark_results"
echo "   • Fichiers temporaires"
echo "   • Logs de test"
echo "   • Rapports de couverture"
echo ""
echo "🎯 Prochaines étapes recommandées :"
echo "   • pytest tests/ -v (relancer les tests)"
echo "   • git add . && git commit -m '🧹 Clean tests'"
echo ""

log_success "🧹 Nettoyage automatique terminé avec succès !" 