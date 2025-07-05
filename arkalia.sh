#!/bin/bash
# 🌕 ARKALIA-LUNA - LANCEUR UNIFIÉ
# Version : 2.8.1 - Pack Pro

set -e

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}🌕 ARKALIA-LUNA - LANCEUR UNIFIÉ${NC}"
    echo -e "${PURPLE}==============================${NC}"
    echo ""
}

print_help() {
    echo "Usage: $0 [COMMANDE]"
    echo ""
    echo "Commandes disponibles:"
    echo "  start       - Démarrer Arkalia-LUNA"
    echo "  test        - Lancer tous les tests"
    echo "  test-fast   - Tests rapides"
    echo "  test-perf   - Tests de performance"
    echo "  clean       - Nettoyer le projet"
    echo "  archive     - Archiver les fichiers temporaires"
    echo "  purge       - Supprimer les archives obsolètes"
    echo "  consolidate - Consolider la structure"
    echo "  build       - Construire le projet"
    echo "  deploy      - Déployer"
    echo "  help        - Afficher cette aide"
    echo ""
}

case "$1" in
    start)
        print_header
        echo -e "${GREEN}🚀 Démarrage d'Arkalia-LUNA...${NC}"
        python run_arkalia_api.py
        ;;
    test)
        print_header
        echo -e "${GREEN}🧪 Lancement de tous les tests...${NC}"
        ./ark-test-full.sh
        ;;
    test-fast)
        print_header
        echo -e "${GREEN}⚡ Tests rapides...${NC}"
        python -m pytest tests/unit/ -v --tb=short
        ;;
    test-perf)
        print_header
        echo -e "${GREEN}📊 Tests de performance...${NC}"
        ./ark-test-performance.sh
        ;;
    clean)
        print_header
        echo -e "${GREEN}🧹 Nettoyage du projet...${NC}"
        ./ark-clean.sh
        ;;
    archive)
        print_header
        echo -e "${GREEN}📦 Archivage des fichiers temporaires...${NC}"
        ./ark-archive.sh
        ;;
    purge)
        print_header
        echo -e "${GREEN}🗑️  Suppression des archives obsolètes...${NC}"
        ./ark-purge-archive.sh --force
        ;;
    consolidate)
        print_header
        echo -e "${GREEN}🔧 Consolidation de la structure...${NC}"
        ./ark-consolidate.sh --force
        ;;
    build)
        print_header
        echo -e "${GREEN}🔨 Construction du projet...${NC}"
        docker-compose build
        ;;
    deploy)
        print_header
        echo -e "${GREEN}🚀 Déploiement...${NC}"
        docker-compose up -d
        ;;
    help|*)
        print_help
        ;;
esac
