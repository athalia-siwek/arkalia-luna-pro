#!/bin/bash
# 🔍 Script de Validation des Dockerfiles - Arkalia-LUNA Pro
# Valide l'existence et la syntaxe de tous les Dockerfiles requis

set -e

echo "🔍 [VALIDATION] Démarrage de la validation des Dockerfiles..."

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de validation d'un Dockerfile
validate_dockerfile() {
    local dockerfile=$1
    local description=$2

    echo -e "${BLUE}🔍 Validation de $dockerfile ($description)...${NC}"

    if [ ! -f "$dockerfile" ]; then
        echo -e "${RED}❌ $dockerfile manquant${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ $dockerfile trouvé${NC}"

    # Validation syntaxe basique
    if ! grep -q "FROM" "$dockerfile"; then
        echo -e "${RED}❌ $dockerfile : instruction FROM manquante${NC}"
        return 1
    fi

    if ! grep -q "COPY\|ADD" "$dockerfile"; then
        echo -e "${YELLOW}⚠️ $dockerfile : aucune instruction COPY/ADD détectée${NC}"
    fi

    if ! grep -q "RUN\|CMD\|ENTRYPOINT" "$dockerfile"; then
        echo -e "${YELLOW}⚠️ $dockerfile : aucune instruction RUN/CMD/ENTRYPOINT détectée${NC}"
    fi

    # Validation syntaxe Docker
    if ! docker build --dry-run -f "$dockerfile" . > /dev/null 2>&1; then
        echo -e "${RED}❌ $dockerfile : syntaxe Docker invalide${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ $dockerfile syntaxe valide${NC}"
    return 0
}

# Liste des Dockerfiles requis avec descriptions
declare -A dockerfiles=(
    ["Dockerfile.zeroia"]="ZeroIA - Décisionneur Autonome"
    ["Dockerfile.reflexia"]="ReflexIA - Observateur Cognitif"
    ["Dockerfile.sandozia"]="Sandozia - Intelligence Croisée"
    ["Dockerfile.assistantia"]="AssistantIA - Assistant IA"
    ["Dockerfile.cognitive-reactor"]="Cognitive Reactor - Intelligence Avancée"
    ["Dockerfile.generative-ai"]="Generative AI - Génération IA"
    ["Dockerfile.master"]="Arkalia Master - Orchestrateur Principal"
    ["modules/cognitive_reactor/Dockerfile"]="Cognitive Reactor (module)"
    ["modules/crossmodule_validator/Dockerfile"]="Crossmodule Validator (module)"
    ["modules/error_recovery/Dockerfile"]="Error Recovery (module)"
)

# Validation de tous les Dockerfiles
errors=0
for dockerfile in "${!dockerfiles[@]}"; do
    if ! validate_dockerfile "$dockerfile" "${dockerfiles[$dockerfile]}"; then
        errors=$((errors + 1))
    fi
done

# Validation docker-compose.yml
echo -e "\n${BLUE}🔍 Validation docker-compose.yml...${NC}"
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml manquant${NC}"
    errors=$((errors + 1))
else
    echo -e "${GREEN}✅ docker-compose.yml trouvé${NC}"

    # Validation syntaxe docker-compose
    if ! docker compose config --quiet > /dev/null 2>&1; then
        echo -e "${RED}❌ docker-compose.yml syntaxe invalide${NC}"
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ docker-compose.yml syntaxe valide${NC}"
    fi
fi

# Résumé
echo -e "\n${BLUE}📊 Résumé de la validation :${NC}"
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les Dockerfiles sont valides !${NC}"
    exit 0
else
    echo -e "${RED}❌ $errors erreur(s) détectée(s)${NC}"
    exit 1
fi
