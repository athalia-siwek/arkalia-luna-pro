#!/bin/bash

# 🐳 Script de test des constructions Docker locales
# Usage: ./scripts/test-docker-builds.sh [image_name]

set -e

echo "🐳 Test des constructions Docker locales Arkalia-LUNA"
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

# Images à tester
IMAGES=("assistantia" "zeroia" "reflexia" "sandozia")
DOCKERFILES=("Dockerfile.assistantia" "Dockerfile.zeroia" "Dockerfile.reflexia" "Dockerfile.sandozia")

# Si un argument est fourni, tester seulement cette image
if [ $# -eq 1 ]; then
    if [[ " ${IMAGES[@]} " =~ " ${1} " ]]; then
        IMAGES=("$1")
        case "$1" in
            "assistantia") DOCKERFILES=("Dockerfile.assistantia") ;;
            "zeroia") DOCKERFILES=("Dockerfile.zeroia") ;;
            "reflexia") DOCKERFILES=("Dockerfile.reflexia") ;;
            "sandozia") DOCKERFILES=("Dockerfile.sandozia") ;;
        esac
        log_info "Test de l'image: $1"
    else
        log_error "Image inconnue: $1"
        log_info "Images disponibles: ${IMAGES[*]}"
        exit 1
    fi
fi

# Nettoyage des images de test
cleanup_test_images() {
    log_info "Nettoyage des images de test..."
    for image in "${IMAGES[@]}"; do
        docker rmi "test-$image" &> /dev/null || true
    done
}

# Gestion de l'interruption
trap cleanup_test_images EXIT

# Vérification de Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker non installé"
    exit 1
fi

if ! docker info &> /dev/null; then
    log_error "Docker daemon non accessible"
    exit 1
fi

log_success "Docker disponible et fonctionnel"

# Test de chaque image
for i in "${!IMAGES[@]}"; do
    image="${IMAGES[$i]}"
    dockerfile="${DOCKERFILES[$i]}"

    echo ""
    log_info "Test de l'image: $image"
    echo "----------------------------------------"

    # Vérification du Dockerfile
    if [ ! -f "$dockerfile" ]; then
        log_error "Dockerfile manquant: $dockerfile"
        continue
    fi

    log_success "Dockerfile trouvé: $dockerfile"

    # Vérification de la syntaxe
    log_info "Vérification de la syntaxe..."
    if docker build --dry-run -f "$dockerfile" . &> /dev/null; then
        log_success "Syntaxe valide"
    else
        log_warning "Problème de syntaxe détecté"
    fi

    # Construction de l'image
    log_info "Construction de l'image test-$image..."
    start_time=$(date +%s)

    if timeout 600 docker build -f "$dockerfile" -t "test-$image" .; then
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        log_success "Construction réussie en ${duration}s"

        # Vérification de la taille de l'image
        image_size=$(docker images "test-$image" --format "table {{.Size}}" | tail -n 1)
        log_info "Taille de l'image: $image_size"

        # Test de démarrage du conteneur
        log_info "Test de démarrage du conteneur..."
        if docker run --rm -d --name "test-$image-container" "test-$image" &> /dev/null; then
            log_success "Conteneur démarré avec succès"

            # Attendre un peu pour voir si le conteneur reste stable
            sleep 5

            # Vérifier si le conteneur fonctionne toujours
            if docker ps | grep -q "test-$image-container"; then
                log_success "Conteneur stable"

                # Test de santé si applicable
                case "$image" in
                    "assistantia")
                        log_info "Test de santé assistantia..."
                        if docker exec "test-$image-container" python -c "import sys; sys.exit(0)" &> /dev/null; then
                            log_success "Python fonctionnel dans assistantia"
                        else
                            log_warning "Python non fonctionnel dans assistantia"
                        fi
                        ;;
                    "zeroia")
                        log_info "Test de santé zeroia..."
                        if docker exec "test-$image-container" python -c "import sys; sys.exit(0)" &> /dev/null; then
                            log_success "Python fonctionnel dans zeroia"
                        else
                            log_warning "Python non fonctionnel dans zeroia"
                        fi
                        ;;
                    "reflexia")
                        log_info "Test de santé reflexia..."
                        if docker exec "test-$image-container" python -c "import sys; sys.exit(0)" &> /dev/null; then
                            log_success "Python fonctionnel dans reflexia"
                        else
                            log_warning "Python non fonctionnel dans reflexia"
                        fi
                        ;;
                    "sandozia")
                        log_info "Test de santé sandozia..."
                        if docker exec "test-$image-container" python -c "import sys; sys.exit(0)" &> /dev/null; then
                            log_success "Python fonctionnel dans sandozia"
                        else
                            log_warning "Python non fonctionnel dans sandozia"
                        fi
                        ;;
                esac
            else
                log_error "Conteneur arrêté prématurément"
            fi

            # Arrêt du conteneur
            docker stop "test-$image-container" &> /dev/null || true
        else
            log_error "Échec du démarrage du conteneur"
        fi

    else
        log_error "Échec de la construction"

        # Affichage des logs d'erreur
        log_info "Logs d'erreur de la construction:"
        docker build -f "$dockerfile" -t "test-$image" . 2>&1 | tail -20 || true
    fi
done

echo ""
log_success "Tests de construction terminés!"

# Rapport final
echo ""
log_info "Rapport final:"
echo "==============="

for image in "${IMAGES[@]}"; do
    if docker images | grep -q "test-$image"; then
        log_success "$image: Construction réussie"
    else
        log_error "$image: Construction échouée"
    fi
done

echo ""
log_info "Recommandations:"
echo "=================="

# Vérification des ressources
memory_gb=$(free -g | awk '/^Mem:/{print $2}')
if [ "$memory_gb" -lt 8 ]; then
    log_warning "Mémoire faible (${memory_gb}GB). Recommandé: 8GB+ pour les builds Docker"
fi

disk_gb=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$disk_gb" -lt 20 ]; then
    log_warning "Espace disque faible (${disk_gb}GB). Recommandé: 20GB+ pour les images Docker"
fi

echo ""
log_info "Pour résoudre les problèmes de build:"
echo "- Vérifiez les dépendances dans requirements.txt"
echo "- Assurez-vous que tous les fichiers sont présents"
echo "- Augmentez les timeouts si nécessaire"
echo "- Utilisez le cache Docker pour accélérer les builds"
