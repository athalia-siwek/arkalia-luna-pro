#!/bin/bash

# ════════════════════════════════════════════════════════════════════════════
# 🚀 ARKALIA-LUNA CONTAINERS MANAGEMENT - VERSION SIMPLE & SAFE
# Script simplifié de gestion des conteneurs Docker
# ════════════════════════════════════════════════════════════════════════════

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Variables
COMPOSE_FILE="docker-compose.simple.yml"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ════════════════════════════════════════════════════════════════════════════
# FONCTIONS PRINCIPALES
# ════════════════════════════════════════════════════════════════════════════

start_containers() {
    log_info "🚀 Démarrage des conteneurs Arkalia-LUNA..."

    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Fichier $COMPOSE_FILE introuvable"
        return 1
    fi

    # Nettoyage préalable
    find . -name "._*" -delete 2>/dev/null || true
    find . -name ".DS_Store" -delete 2>/dev/null || true

    # Construction et démarrage
    docker compose -f "$COMPOSE_FILE" build --no-cache
    docker compose -f "$COMPOSE_FILE" up -d

    log_info "✅ Conteneurs démarrés"
    log_info "🌐 API disponible sur: http://localhost:8000"
    log_info "🤖 AssistantIA disponible sur: http://localhost:8001"
}

stop_containers() {
    log_info "🛑 Arrêt des conteneurs..."
    docker compose -f "$COMPOSE_FILE" down -v || true
    log_info "✅ Conteneurs arrêtés"
}

rebuild_containers() {
    log_info "🔄 Reconstruction des conteneurs..."
    stop_containers
    docker system prune -f || true
    start_containers
}

show_status() {
    log_info "📊 Statut des conteneurs..."
    echo ""
    docker compose -f "$COMPOSE_FILE" ps
    echo ""

    # Test de connectivité
    if curl -s -f http://localhost:8000/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} API (port 8000) - Fonctionnelle"
    else
        echo -e "  ${RED}❌${NC} API (port 8000) - Non disponible"
    fi

    if curl -s -f http://localhost:8001/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} AssistantIA (port 8001) - Fonctionnelle"
    else
        echo -e "  ${RED}❌${NC} AssistantIA (port 8001) - Non disponible"
    fi
}

show_logs() {
    local service=${1:-""}
    if [[ -n "$service" ]]; then
        log_info "📋 Logs du service: $service"
        docker compose -f "$COMPOSE_FILE" logs -f --tail=100 "$service"
    else
        log_info "📋 Logs de tous les services"
        docker compose -f "$COMPOSE_FILE" logs -f --tail=50
    fi
}

health_check() {
    log_info "🏥 Vérification de santé..."

    local all_healthy=true

    # Test des services
    if docker compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        echo -e "  ${GREEN}✅${NC} Services Docker - Running"
    else
        echo -e "  ${RED}❌${NC} Services Docker - Stopped"
        all_healthy=false
    fi

    # Test des endpoints
    if curl -s -f http://localhost:8000/health &>/dev/null; then
        echo -e "  ${GREEN}✅${NC} API Health Check"
    else
        echo -e "  ${RED}❌${NC} API Health Check"
        all_healthy=false
    fi

    if $all_healthy; then
        log_info "✅ Système en bonne santé"
    else
        log_warn "⚠️ Problèmes détectés"
    fi
}

show_help() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}              ARKALIA-LUNA CONTAINERS MANAGER (SIMPLE)            ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e ""
    echo -e "${YELLOW}Commandes disponibles:${NC}"
    echo -e ""
    echo -e "  ${GREEN}start${NC}     Démarrer tous les conteneurs"
    echo -e "  ${GREEN}stop${NC}      Arrêter tous les conteneurs"
    echo -e "  ${GREEN}rebuild${NC}   Reconstruction complète"
    echo -e "  ${GREEN}status${NC}    Afficher le statut"
    echo -e "  ${GREEN}logs${NC}      Voir les logs"
    echo -e "  ${GREEN}health${NC}    Vérification de santé"
    echo -e "  ${GREEN}help${NC}      Afficher cette aide"
    echo -e ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

case "${1:-help}" in
    "start")        start_containers ;;
    "stop")         stop_containers ;;
    "rebuild")      rebuild_containers ;;
    "status")       show_status ;;
    "logs")         show_logs "${2:-}" ;;
    "health")       health_check ;;
    "help"|*)       show_help ;;
esac
