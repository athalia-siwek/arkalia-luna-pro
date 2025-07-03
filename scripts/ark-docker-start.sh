#!/bin/bash

# 🚀 Arkalia-LUNA Pro — Script de démarrage Docker v2.8.0
# Démarre tous les services Arkalia en mode Docker

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

echo -e "${PURPLE}🌕 Arkalia-LUNA Pro — Démarrage Docker v2.8.0${NC}"
echo -e "${CYAN}================================================${NC}"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    exit 1
fi

# Vérifier que Docker Desktop est démarré
if ! docker info &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Desktop n'est pas démarré${NC}"
    echo -e "${YELLOW}🔄 Démarrage de Docker Desktop...${NC}"

    # Essayer de démarrer Docker Desktop sur macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker
        echo -e "${YELLOW}⏳ Attente du démarrage de Docker...${NC}"
        sleep 30

        # Vérifier si Docker est maintenant disponible
        if ! docker info &> /dev/null; then
            echo -e "${RED}❌ Impossible de démarrer Docker Desktop${NC}"
            echo -e "${YELLOW}💡 Veuillez démarrer Docker Desktop manuellement${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Veuillez démarrer Docker manuellement${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Docker est prêt${NC}"

# Aller dans le répertoire du projet
cd "$PROJECT_ROOT"

# Vérifier que le fichier docker-compose.yml existe
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo -e "${RED}❌ Fichier docker-compose.yml introuvable${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Vérification de l'environnement...${NC}"

# Vérifier les variables d'environnement
export PORT_API=${PORT_API:-8000}
export PORT_ASSISTANTIA=${PORT_ASSISTANTIA:-8001}
export PORT_REFLEXIA=${PORT_REFLEXIA:-8002}
export PORT_COGNITIVE=${PORT_COGNITIVE:-8003}

echo -e "${GREEN}✅ Ports configurés:${NC}"
echo -e "   🚀 Arkalia API: $PORT_API"
echo -e "   🤖 AssistantIA: $PORT_ASSISTANTIA"
echo -e "   🔁 Reflexia: $PORT_REFLEXIA"
echo -e "   🧠 Cognitive: $PORT_COGNITIVE"

# Arrêter les services existants s'ils tournent
echo -e "${BLUE}🛑 Arrêt des services existants...${NC}"
docker compose -f "$COMPOSE_FILE" down --remove-orphans 2>/dev/null || true

# Nettoyer les conteneurs orphelins
echo -e "${BLUE}🧹 Nettoyage des conteneurs orphelins...${NC}"
docker container prune -f 2>/dev/null || true

# Construire les images
echo -e "${BLUE}🔨 Construction des images Docker...${NC}"
docker compose -f "$COMPOSE_FILE" build --no-cache

# Démarrer les services
echo -e "${BLUE}🚀 Démarrage des services Arkalia...${NC}"
docker compose -f "$COMPOSE_FILE" up -d

# Attendre que les services démarrent
echo -e "${YELLOW}⏳ Attente du démarrage des services...${NC}"
sleep 30

# Vérifier l'état des services
echo -e "${BLUE}🔍 Vérification de l'état des services...${NC}"
docker compose -f "$COMPOSE_FILE" ps

# Tests de santé
echo -e "${BLUE}🏥 Tests de santé des services...${NC}"

# Test AssistantIA
if curl -s http://localhost:$PORT_ASSISTANTIA/api/v1/health > /dev/null; then
    echo -e "${GREEN}✅ AssistantIA: Opérationnel${NC}"
else
    echo -e "${RED}❌ AssistantIA: Erreur${NC}"
fi

# Test Arkalia API
if curl -s http://localhost:$PORT_API/health > /dev/null; then
    echo -e "${GREEN}✅ Arkalia API: Opérationnel${NC}"
else
    echo -e "${RED}❌ Arkalia API: Erreur${NC}"
fi

# Test Reflexia
if curl -s http://localhost:$PORT_REFLEXIA/health > /dev/null; then
    echo -e "${GREEN}✅ Reflexia: Opérationnel${NC}"
else
    echo -e "${YELLOW}⚠️  Reflexia: Non testé (port non exposé)${NC}"
fi

echo -e "${PURPLE}🎉 Démarrage Docker terminé !${NC}"
echo -e "${CYAN}================================================${NC}"
echo -e "${GREEN}🌐 URLs des services:${NC}"
echo -e "   🚀 Arkalia API: http://localhost:$PORT_API"
echo -e "   🤖 AssistantIA: http://localhost:$PORT_ASSISTANTIA"
echo -e "   🔁 Reflexia: http://localhost:$PORT_REFLEXIA"
echo -e "   🧠 Cognitive: http://localhost:$PORT_COGNITIVE"
echo -e ""
echo -e "${YELLOW}📋 Commandes utiles:${NC}"
echo -e "   📊 État des services: docker compose ps"
echo -e "   📝 Logs: docker compose logs -f"
echo -e "   🛑 Arrêt: docker compose down"
echo -e "   🔄 Redémarrage: docker compose restart"
echo -e ""
echo -e "${GREEN}🌟 Arkalia-LUNA Pro est prêt !${NC}"
