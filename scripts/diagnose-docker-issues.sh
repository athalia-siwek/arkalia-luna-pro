#!/bin/bash

# 🔍 Script de diagnostic des problèmes Docker et réseau
# Usage: ./scripts/diagnose-docker-issues.sh

set -e

echo "🔍 Diagnostic des problèmes Docker et réseau Arkalia-LUNA"
echo "========================================================"
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

# 1. Vérification de Docker
log_info "1. Vérification de Docker..."
if command -v docker &> /dev/null; then
    log_success "Docker installé"
    docker_version=$(docker --version)
    log_info "Version: $docker_version"

    if docker info &> /dev/null; then
        log_success "Docker daemon fonctionnel"
    else
        log_error "Docker daemon non accessible"
        exit 1
    fi
else
    log_error "Docker non installé"
    exit 1
fi

# 2. Vérification de Docker Compose
log_info "2. Vérification de Docker Compose..."
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    log_success "Docker Compose disponible"
    if docker compose version &> /dev/null; then
        compose_version=$(docker compose version --short)
        log_info "Version: $compose_version"
    fi
else
    log_error "Docker Compose non disponible"
    exit 1
fi

# 3. Vérification de la connectivité réseau
log_info "3. Vérification de la connectivité réseau..."

# Test GitHub Container Registry
log_info "Test de connexion à ghcr.io..."
if curl -f -s --max-time 10 "https://ghcr.io/v2/" > /dev/null; then
    log_success "Connexion à ghcr.io réussie"
else
    log_warning "Connexion à ghcr.io échouée"
    log_info "Tentative avec timeout plus long..."
    if curl -f -s --max-time 30 "https://ghcr.io/v2/" > /dev/null; then
        log_success "Connexion à ghcr.io réussie avec timeout étendu"
    else
        log_error "Connexion à ghcr.io échouée même avec timeout étendu"
    fi
fi

# Test GitHub API
log_info "Test de connexion à GitHub API..."
if curl -f -s --max-time 10 "https://api.github.com" > /dev/null; then
    log_success "Connexion à GitHub API réussie"
else
    log_warning "Connexion à GitHub API échouée"
fi

# 4. Vérification des Dockerfiles
log_info "4. Vérification des Dockerfiles..."
dockerfiles=("Dockerfile.zeroia" "Dockerfile.reflexia" "Dockerfile.sandozia" "Dockerfile.assistantia")
missing_files=()

for dockerfile in "${dockerfiles[@]}"; do
    if [ -f "$dockerfile" ]; then
        log_success "$dockerfile trouvé"

        # Vérification basique de la syntaxe
        if docker build --help &> /dev/null; then
            log_success "Docker build disponible pour $dockerfile"
        else
            log_warning "Docker build non disponible"
        fi
    else
        log_error "$dockerfile manquant"
        missing_files+=("$dockerfile")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    log_error "Dockerfiles manquants: ${missing_files[*]}"
fi

# 5. Vérification de docker-compose.yml
log_info "5. Vérification de docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    log_success "docker-compose.yml trouvé"

    if docker compose config --quiet; then
        log_success "Configuration docker-compose.yml valide"
    else
        log_error "Configuration docker-compose.yml invalide"
    fi
else
    log_error "docker-compose.yml manquant"
fi

# 6. Vérification des ressources système
log_info "6. Vérification des ressources système..."

# Mémoire disponible
memory_gb=$(free -g | awk '/^Mem:/{print $2}')
if [ "$memory_gb" -ge 4 ]; then
    log_success "Mémoire suffisante: ${memory_gb}GB"
else
    log_warning "Mémoire faible: ${memory_gb}GB (recommandé: 4GB+)"
fi

# Espace disque
disk_gb=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$disk_gb" -ge 10 ]; then
    log_success "Espace disque suffisant: ${disk_gb}GB"
else
    log_warning "Espace disque faible: ${disk_gb}GB (recommandé: 10GB+)"
fi

# 7. Vérification des permissions
log_info "7. Vérification des permissions..."
if docker run --rm hello-world &> /dev/null; then
    log_success "Permissions Docker correctes"
else
    log_error "Problème de permissions Docker"
    log_info "Essayez: sudo usermod -aG docker $USER"
fi

# 8. Test de construction locale
log_info "8. Test de construction locale (assistantia)..."
if [ -f "Dockerfile.assistantia" ]; then
    log_info "Construction de l'image assistantia (test local)..."
    if timeout 300 docker build -f Dockerfile.assistantia -t test-assistantia . &> /dev/null; then
        log_success "Construction locale réussie"
        docker rmi test-assistantia &> /dev/null || true
    else
        log_error "Construction locale échouée"
    fi
else
    log_warning "Dockerfile.assistantia non trouvé, test de construction ignoré"
fi

# 9. Recommandations
echo ""
log_info "9. Recommandations pour résoudre les problèmes:"
echo ""

if ! curl -f -s --max-time 10 "https://ghcr.io/v2/" > /dev/null; then
    echo "🌐 Problèmes de réseau:"
    echo "   - Vérifiez votre connexion internet"
    echo "   - Essayez avec un VPN si nécessaire"
    echo "   - Augmentez les timeouts dans les workflows GitHub"
    echo ""
fi

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "📁 Fichiers manquants:"
    echo "   - Restaurez les Dockerfiles manquants depuis l'archive"
    echo "   - Vérifiez que tous les fichiers sont commités"
    echo ""
fi

echo "🔧 Optimisations générales:"
echo "   - Utilisez le workflow optimisé: .github/workflows/deploy-optimized.yml"
echo "   - Augmentez les timeouts dans les actions GitHub"
echo "   - Utilisez le cache Docker pour accélérer les builds"
echo "   - Vérifiez les permissions GitHub Actions"
echo ""

# 10. Test de démarrage des services
log_info "10. Test de démarrage des services..."
if [ -f "docker-compose.yml" ]; then
    log_info "Démarrage des services (test rapide)..."
    if timeout 120 docker compose up -d --remove-orphans &> /dev/null; then
        log_success "Services démarrés avec succès"

        # Test de santé rapide
        sleep 10
        if curl -f -s --max-time 10 "http://localhost:8000/health" > /dev/null; then
            log_success "API principale accessible"
        else
            log_warning "API principale non accessible"
        fi

        # Arrêt des services
        docker compose down --remove-orphans &> /dev/null || true
    else
        log_error "Échec du démarrage des services"
    fi
else
    log_warning "docker-compose.yml non trouvé, test de démarrage ignoré"
fi

echo ""
log_success "Diagnostic terminé!"
echo ""
log_info "Pour plus d'informations, consultez:"
echo "   - Les logs GitHub Actions"
echo "   - La documentation de déploiement"
echo "   - Les rapports de nettoyage dans archive/"
