#!/bin/bash

# 🔄 Script de basculement vers le workflow optimisé
# Usage: ./scripts/switch-to-optimized-workflow.sh

set -e

echo "🔄 Basculement vers le workflow optimisé Arkalia-LUNA"
echo "===================================================="
echo ""

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

# Vérification des prérequis
log_info "Vérification des prérequis..."

if [ ! -f ".github/workflows/deploy.yml" ]; then
    log_error "Workflow actuel non trouvé: .github/workflows/deploy.yml"
    exit 1
fi

if [ ! -f ".github/workflows/deploy-optimized.yml" ]; then
    log_error "Workflow optimisé non trouvé: .github/workflows/deploy-optimized.yml"
    exit 1
fi

log_success "Fichiers de workflow trouvés"

# Sauvegarde du workflow actuel
log_info "Sauvegarde du workflow actuel..."
if [ -f ".github/workflows/deploy-backup.yml" ]; then
    log_warning "Backup existant détecté, remplacement..."
    rm .github/workflows/deploy-backup.yml
fi

cp .github/workflows/deploy.yml .github/workflows/deploy-backup.yml
log_success "Workflow actuel sauvegardé: .github/workflows/deploy-backup.yml"

# Remplacement par le workflow optimisé
log_info "Remplacement par le workflow optimisé..."
cp .github/workflows/deploy-optimized.yml .github/workflows/deploy.yml
log_success "Workflow optimisé installé: .github/workflows/deploy.yml"

# Vérification de la syntaxe
log_info "Vérification de la syntaxe du nouveau workflow..."
if command -v yamllint &> /dev/null; then
    if yamllint .github/workflows/deploy.yml; then
        log_success "Syntaxe YAML valide"
    else
        log_warning "Problème de syntaxe YAML détecté"
    fi
else
    log_warning "yamllint non disponible, vérification manuelle recommandée"
fi

# Affichage des différences principales
echo ""
log_info "Principales améliorations du workflow optimisé:"
echo "=================================================="
echo "✅ Timeouts augmentés:"
echo "   - Build: 30min → 60min"
echo "   - Push: 15min → 45min"
echo "   - E2E: 45min → 60min"
echo ""
echo "✅ Retry logic améliorée:"
echo "   - Health checks: 10 tentatives → 15 tentatives"
echo "   - Timeout par tentative: 10s → 30s"
echo "   - Intervalle entre tentatives: 10s → 15s"
echo ""
echo "✅ Cache Docker optimisé:"
echo "   - Compression gzip activée"
echo "   - Debug flags pour BuildKit"
echo "   - Cache local amélioré"
echo ""
echo "✅ Gestion d'erreurs renforcée:"
echo "   - Validation manuelle des Dockerfiles"
echo "   - Vérification des images construites"
echo "   - Rapports détaillés d'échec"

# Test de validation
echo ""
log_info "Test de validation du workflow..."
if [ -f "scripts/diagnose-docker-issues.sh" ]; then
    log_info "Exécution du diagnostic Docker..."
    ./scripts/diagnose-docker-issues.sh | head -20
    log_success "Diagnostic Docker terminé"
else
    log_warning "Script de diagnostic non trouvé"
fi

# Instructions pour le déploiement
echo ""
log_info "Instructions pour le déploiement:"
echo "===================================="
echo ""
echo "1. Commitez les changements:"
echo "   git add .github/workflows/deploy.yml"
echo "   git commit -m 'feat: switch to optimized Docker workflow'"
echo ""
echo "2. Poussez vers GitHub:"
echo "   git push origin dev-migration"
echo ""
echo "3. Surveillez le déploiement:"
echo "   - Allez sur GitHub Actions"
echo "   - Vérifiez le workflow 'Deploy Arkalia-LUNA'"
echo "   - Surveillez les logs en temps réel"
echo ""
echo "4. En cas de problème:"
echo "   - Restaurez le backup: mv .github/workflows/deploy-backup.yml .github/workflows/deploy.yml"
echo "   - Consultez les logs d'erreur"
echo "   - Exécutez: ./scripts/diagnose-docker-issues.sh"

# Vérification finale
echo ""
log_info "Vérification finale..."
if [ -f ".github/workflows/deploy.yml" ] && [ -f ".github/workflows/deploy-backup.yml" ]; then
    log_success "Basculement réussi!"
    log_info "Workflow actuel: .github/workflows/deploy.yml"
    log_info "Backup: .github/workflows/deploy-backup.yml"
else
    log_error "Problème lors du basculement"
    exit 1
fi

echo ""
log_success "Basculement vers le workflow optimisé terminé!"
log_info "Le prochain push déclenchera le nouveau workflow avec des timeouts augmentés." 