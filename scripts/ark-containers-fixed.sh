#!/bin/bash

# ════════════════════════════════════════════════════════════════════════════
# 🚀 ARKALIA-LUNA CONTAINERS MANAGEMENT - VERSION FIXED
# Script de gestion des conteneurs Docker optimisés et corrigés
# ════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# Variables globales
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
readonly PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
readonly COMPOSE_FILE="$PROJECT_DIR/docker-compose.fixed.yml"
readonly LOG_FILE="$PROJECT_DIR/logs/containers_fixed.log"

# Couleurs pour la sortie
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# ════════════════════════════════════════════════════════════════════════════
# 🛠️ FONCTIONS UTILITAIRES
# ════════════════════════════════════════════════════════════════════════════

log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case $level in
        "INFO")  echo -e "${GREEN}[INFO]${NC} $message" ;;
        "WARN")  echo -e "${YELLOW}[WARN]${NC} $message" ;;
        "ERROR") echo -e "${RED}[ERROR]${NC} $message" ;;
        "DEBUG") echo -e "${BLUE}[DEBUG]${NC} $message" ;;
        *)       echo -e "${CYAN}[LOG]${NC} $message" ;;
    esac

    # Log vers fichier
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

check_requirements() {
    log "INFO" "🔍 Vérification des prérequis..."

    if ! command -v docker &> /dev/null; then
        log "ERROR" "Docker n'est pas installé"
        exit 1
    fi

    if ! command -v docker compose &> /dev/null; then
        log "ERROR" "Docker Compose n'est pas installé"
        exit 1
    fi

    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log "ERROR" "Fichier docker-compose.fixed.yml introuvable: $COMPOSE_FILE"
        exit 1
    fi

    log "INFO" "✅ Prérequis validés"
}

cleanup_system() {
    log "INFO" "🧹 Nettoyage du système Docker..."

    # Nettoyer les fichiers cachés macOS
    find "$PROJECT_DIR" -name "._*" -delete 2>/dev/null || true
    find "$PROJECT_DIR" -name ".DS_Store" -delete 2>/dev/null || true

    # Nettoyer Docker
    docker system prune -f --volumes || true
    docker builder prune -f || true

    log "INFO" "✅ Nettoyage terminé"
}

# ════════════════════════════════════════════════════════════════════════════
# 🚀 FONCTIONS PRINCIPALES DE GESTION
# ════════════════════════════════════════════════════════════════════════════

ark-start-fixed() {
    log "INFO" "🚀 Démarrage des conteneurs Arkalia-LUNA (FIXED)..."
    check_requirements

    # Nettoyage préalable
    cleanup_system

    # Construire et démarrer
    log "INFO" "🔨 Construction des images..."
    docker compose -f "$COMPOSE_FILE" build --no-cache

    log "INFO" "▶️ Démarrage des services..."
    docker compose -f "$COMPOSE_FILE" up -d

    # Attendre que les services soient prêts
    log "INFO" "⏳ Attente de la disponibilité des services..."
    sleep 15

    # Vérifier le statut
    ark-status-fixed

    log "INFO" "✅ Tous les conteneurs sont démarrés !"
    log "INFO" "🌐 API disponible sur: http://localhost:8000"
    log "INFO" "🤖 AssistantIA disponible sur: http://localhost:8001"
}

ark-stop-fixed() {
    log "INFO" "🛑 Arrêt des conteneurs Arkalia-LUNA (FIXED)..."

    docker compose -f "$COMPOSE_FILE" down -v || true

    log "INFO" "✅ Tous les conteneurs sont arrêtés"
}

ark-rebuild-fixed() {
    log "INFO" "🔄 Reconstruction complète des conteneurs..."

    # Arrêt complet
    ark-stop-fixed

    # Nettoyage approfondi
    cleanup_system

    # Supprimer les images existantes
    log "INFO" "🗑️ Suppression des anciennes images..."
    docker images | grep arkalia-luna-pro | awk '{print $3}' | xargs -r docker rmi -f || true

    # Redémarrage
    ark-start-fixed

    log "INFO" "✅ Reconstruction terminée"
}

ark-status-fixed() {
    log "INFO" "📊 Statut des conteneurs Arkalia-LUNA (FIXED)..."

    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}              ARKALIA-LUNA CONTAINERS STATUS (FIXED)              ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"

    # Statut Docker Compose
    docker compose -f "$COMPOSE_FILE" ps

    echo -e "\n${PURPLE}🔍 Tests de connectivité:${NC}"

    # Test API principale
    if curl -s -f http://localhost:8000/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} API Arkalia (port 8000) - ${GREEN}Fonctionnelle${NC}"
    else
        echo -e "  ${RED}❌${NC} API Arkalia (port 8000) - ${RED}Non disponible${NC}"
    fi

    # Test AssistantIA
    if curl -s -f http://localhost:8001/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} AssistantIA (port 8001) - ${GREEN}Fonctionnelle${NC}"
    else
        echo -e "  ${RED}❌${NC} AssistantIA (port 8001) - ${RED}Non disponible${NC}"
    fi

    # Afficher les tailles des images
    echo -e "\n${PURPLE}📦 Tailles des images:${NC}"
    docker images | grep -E "(arkalia-luna-pro|REPOSITORY)" | head -10

    # Utilisation des ressources
    echo -e "\n${PURPLE}💾 Utilisation des ressources:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" || true

    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

ark-logs-fixed() {
    local service=${1:-""}

    if [[ -n "$service" ]]; then
        log "INFO" "📋 Logs du service: $service"
        docker compose -f "$COMPOSE_FILE" logs -f --tail=100 "$service"
    else
        log "INFO" "📋 Logs de tous les services (temps réel)"
        docker compose -f "$COMPOSE_FILE" logs -f --tail=50
    fi
}

ark-restart-service-fixed() {
    local service=${1:-""}

    if [[ -z "$service" ]]; then
        log "ERROR" "Usage: ark-restart-service-fixed <service_name>"
        log "INFO" "Services disponibles: arkalia-api-fixed, assistantia-fixed, reflexia-fixed, zeroia-fixed, sandozia-fixed, cognitive-reactor-fixed"
        return 1
    fi

    log "INFO" "🔄 Redémarrage du service: $service"
    docker compose -f "$COMPOSE_FILE" restart "$service"

    sleep 5
    docker compose -f "$COMPOSE_FILE" ps "$service"

    log "INFO" "✅ Service $service redémarré"
}

ark-shell-fixed() {
    local service=${1:-"arkalia-api-fixed"}

    log "INFO" "🐚 Ouverture d'un shell dans le conteneur: $service"
    docker compose -f "$COMPOSE_FILE" exec "$service" /bin/bash
}

ark-health-check-fixed() {
    log "INFO" "🏥 Vérification de santé complète..."

    local all_healthy=true

    # Check des services principaux
    services=("arkalia-api-fixed" "assistantia-fixed" "reflexia-fixed" "zeroia-fixed" "sandozia-fixed" "cognitive-reactor-fixed")

    for service in "${services[@]}"; do
        if docker compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
            echo -e "  ${GREEN}✅${NC} $service - Running"
        else
            echo -e "  ${RED}❌${NC} $service - Stopped/Error"
            all_healthy=false
        fi
    done

    # Test des endpoints
    echo -e "\n${PURPLE}🌐 Tests des endpoints:${NC}"

    if curl -s -f http://localhost:8000/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} http://localhost:8000/health"
    else
        echo -e "  ${RED}❌${NC} http://localhost:8000/health"
        all_healthy=false
    fi

    if curl -s -f http://localhost:8001/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} http://localhost:8001/health"
    else
        echo -e "  ${RED}❌${NC} http://localhost:8001/health"
        all_healthy=false
    fi

    if $all_healthy; then
        log "INFO" "✅ Tous les services sont en bonne santé"
        return 0
    else
        log "WARN" "⚠️ Certains services présentent des problèmes"
        return 1
    fi
}

# ════════════════════════════════════════════════════════════════════════════
# 🎯 FONCTION PRINCIPALE
# ════════════════════════════════════════════════════════════════════════════

show_help() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}              ARKALIA-LUNA CONTAINERS MANAGER (FIXED)             ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e ""
    echo -e "${YELLOW}Commandes disponibles:${NC}"
    echo -e ""
    echo -e "  ${GREEN}ark-start-fixed${NC}                    Démarrer tous les conteneurs"
    echo -e "  ${GREEN}ark-stop-fixed${NC}                     Arrêter tous les conteneurs"
    echo -e "  ${GREEN}ark-rebuild-fixed${NC}                  Reconstruction complète"
    echo -e "  ${GREEN}ark-status-fixed${NC}                   Afficher le statut complet"
    echo -e "  ${GREEN}ark-logs-fixed [service]${NC}           Voir les logs (temps réel)"
    echo -e "  ${GREEN}ark-restart-service-fixed <service>${NC} Redémarrer un service"
    echo -e "  ${GREEN}ark-shell-fixed [service]${NC}          Ouvrir un shell dans un conteneur"
    echo -e "  ${GREEN}ark-health-check-fixed${NC}             Vérification de santé complète"
    echo -e ""
    echo -e "${YELLOW}Services disponibles:${NC}"
    echo -e "  • arkalia-api-fixed      (API principale)"
    echo -e "  • assistantia-fixed      (Navigateur IA)"
    echo -e "  • reflexia-fixed         (Observateur cognitif)"
    echo -e "  • zeroia-fixed           (Décideur ultra-rapide)"
    echo -e "  • sandozia-fixed         (Intelligence croisée - CORRIGÉ)"
    echo -e "  • cognitive-reactor-fixed (Réactions automatiques - CORRIGÉ)"
    echo -e ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

main() {
    case "${1:-help}" in
        "ark-start-fixed")        ark-start-fixed ;;
        "ark-stop-fixed")         ark-stop-fixed ;;
        "ark-rebuild-fixed")      ark-rebuild-fixed ;;
        "ark-status-fixed")       ark-status-fixed ;;
        "ark-logs-fixed")         ark-logs-fixed "${2:-}" ;;
        "ark-restart-service-fixed") ark-restart-service-fixed "${2:-}" ;;
        "ark-shell-fixed")        ark-shell-fixed "${2:-}" ;;
        "ark-health-check-fixed") ark-health-check-fixed ;;
        "help"|"--help"|"-h")     show_help ;;
        *)                        show_help ;;
    esac
}

# Permettre l'utilisation directe des fonctions
if [[ "${BASH_SOURCE[0]:-$0}" == "${0}" ]]; then
    main "$@"
fi
