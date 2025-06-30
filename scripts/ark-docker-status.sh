#!/bin/bash

# 📊 Arkalia-LUNA Pro — Script de statut Docker v2.8.0
# Affiche l'état de tous les services Arkalia en mode Docker

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

echo -e "${PURPLE}🌕 Arkalia-LUNA Pro — Statut Docker v2.8.0${NC}"
echo -e "${CYAN}==============================================${NC}"

# Aller dans le répertoire du projet
cd "$PROJECT_ROOT"

# Vérifier que le fichier docker-compose.yml existe
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo -e "${RED}❌ Fichier docker-compose.yml introuvable${NC}"
    exit 1
fi

# Vérifier que Docker est disponible
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas disponible${NC}"
    echo -e "${YELLOW}💡 Démarrez Docker Desktop et réessayez${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker est disponible${NC}"

# Afficher l'état des conteneurs
echo -e "${BLUE}📊 État des conteneurs:${NC}"
docker-compose -f "$COMPOSE_FILE" ps

echo -e ""
echo -e "${BLUE}🔍 Détails des services:${NC}"

# Vérifier chaque service individuellement
services=("arkalia-api" "assistantia" "reflexia" "zeroia" "sandozia" "cognitive-reactor")

for service in "${services[@]}"; do
    if docker-compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
        echo -e "${GREEN}✅ $service: En cours d'exécution${NC}"
    else
        echo -e "${RED}❌ $service: Arrêté${NC}"
    fi
done

echo -e ""
echo -e "${BLUE}🌐 Tests de connectivité:${NC}"

# Variables d'environnement
export PORT_API=${PORT_API:-8000}
export PORT_ASSISTANTIA=${PORT_ASSISTANTIA:-8001}
export PORT_REFLEXIA=${PORT_REFLEXIA:-8002}
export PORT_COGNITIVE=${PORT_COGNITIVE:-8003}

# Test AssistantIA
if curl -s http://localhost:$PORT_ASSISTANTIA/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ AssistantIA (port $PORT_ASSISTANTIA): Répond${NC}"
else
    echo -e "${RED}❌ AssistantIA (port $PORT_ASSISTANTIA): Ne répond pas${NC}"
fi

# Test Arkalia API
if curl -s http://localhost:$PORT_API/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Arkalia API (port $PORT_API): Répond${NC}"
else
    echo -e "${RED}❌ Arkalia API (port $PORT_API): Ne répond pas${NC}"
fi

# Test Reflexia
if curl -s http://localhost:$PORT_REFLEXIA/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Reflexia (port $PORT_REFLEXIA): Répond${NC}"
else
    echo -e "${YELLOW}⚠️  Reflexia (port $PORT_REFLEXIA): Non testé (port non exposé)${NC}"
fi

echo -e ""
echo -e "${BLUE}📈 Utilisation des ressources:${NC}"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo -e ""
echo -e "${CYAN}==============================================${NC}"
echo -e "${YELLOW}📋 Commandes utiles:${NC}"
echo -e "   🚀 Démarrage: ./scripts/ark-docker-start.sh"
echo -e "   🛑 Arrêt: ./scripts/ark-docker-stop.sh"
echo -e "   📝 Logs: docker-compose logs -f"
echo -e "   🔄 Redémarrage: docker-compose restart"
