#!/bin/bash

# 🛑 Arkalia-LUNA Pro — Script d'arrêt Docker v2.8.0
# Arrête tous les services Arkalia en mode Docker

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

echo -e "${PURPLE}🌕 Arkalia-LUNA Pro — Arrêt Docker v2.8.0${NC}"
echo -e "${CYAN}==============================================${NC}"

# Aller dans le répertoire du projet
cd "$PROJECT_ROOT"

# Vérifier que le fichier docker-compose.yml existe
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo -e "${RED}❌ Fichier docker-compose.yml introuvable${NC}"
    exit 1
fi

# Arrêter les services
echo -e "${BLUE}🛑 Arrêt des services Arkalia...${NC}"
docker compose -f "$COMPOSE_FILE" down --remove-orphans

# Nettoyer les conteneurs orphelins
echo -e "${BLUE}🧹 Nettoyage des conteneurs orphelins...${NC}"
docker container prune -f 2>/dev/null || true

# Nettoyer les réseaux non utilisés
echo -e "${BLUE}🌐 Nettoyage des réseaux non utilisés...${NC}"
docker network prune -f 2>/dev/null || true

echo -e "${GREEN}✅ Tous les services ont été arrêtés${NC}"
echo -e "${CYAN}==============================================${NC}"
echo -e "${YELLOW}💡 Pour redémarrer: ./scripts/ark-docker-start.sh${NC}"
