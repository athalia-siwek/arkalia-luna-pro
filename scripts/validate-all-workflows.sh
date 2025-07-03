#!/bin/bash
# 🔍 Script de Validation Complète des Workflows - Arkalia-LUNA Pro
# Valide tous les workflows GitHub Actions et les configurations

set -e

echo "🔍 [VALIDATION COMPLÈTE] Démarrage de la validation des workflows..."

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
errors=0
warnings=0

# Fonction de validation d'un workflow
validate_workflow() {
    local workflow=$1
    local description=$2

    echo -e "${BLUE}🔍 Validation de $workflow ($description)...${NC}"

    if [ ! -f "$workflow" ]; then
        echo -e "${RED}❌ $workflow manquant${NC}"
        errors=$((errors + 1))
        return 1
    fi

    echo -e "${GREEN}✅ $workflow trouvé${NC}"

    # Validation syntaxe YAML
    if ! yamllint "$workflow" > /dev/null 2>&1; then
        echo -e "${RED}❌ $workflow : syntaxe YAML invalide${NC}"
        errors=$((errors + 1))
        return 1
    fi

    # Validation GitHub Actions avec actionlint si disponible
    if command -v actionlint > /dev/null 2>&1; then
        if ! actionlint "$workflow" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠️ $workflow : avertissements actionlint${NC}"
            warnings=$((warnings + 1))
        else
            echo -e "${GREEN}✅ $workflow : validation actionlint OK${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ actionlint non disponible - validation basique uniquement${NC}"
    fi

    echo -e "${GREEN}✅ $workflow syntaxe valide${NC}"
    return 0
}

# Fonction de validation des Dockerfiles
validate_dockerfiles() {
    echo -e "\n${BLUE}🔍 Validation des Dockerfiles...${NC}"

    # Liste des Dockerfiles requis
    dockerfiles=(
        "Dockerfile.zeroia:ZeroIA - Décisionneur Autonome"
        "Dockerfile-reflexia:ReflexIA - Observateur Cognitif"
        "Dockerfile.sandozia:Sandozia - Intelligence Croisée"
        "Dockerfile.assistantia:AssistantIA - Assistant IA"
        "Dockerfile.cognitive-reactor:Cognitive Reactor - Intelligence Avancée"
        "Dockerfile.generative-ai:Generative AI - Génération IA"
        "Dockerfile.master:Arkalia Master - Orchestrateur Principal"
    )

    for dockerfile_info in "${dockerfiles[@]}"; do
        IFS=':' read -r dockerfile description <<< "$dockerfile_info"

        if [ ! -f "$dockerfile" ]; then
            echo -e "${RED}❌ $dockerfile manquant${NC}"
            errors=$((errors + 1))
        else
            echo -e "${GREEN}✅ $dockerfile trouvé${NC}"

            # Validation syntaxe basique
            if ! grep -q "FROM" "$dockerfile"; then
                echo -e "${RED}❌ $dockerfile : instruction FROM manquante${NC}"
                errors=$((errors + 1))
            fi
        fi
    done
}

# Fonction de validation docker-compose
validate_docker_compose() {
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
}

# Fonction de validation MkDocs
validate_mkdocs() {
    echo -e "\n${BLUE}🔍 Validation MkDocs...${NC}"

    if [ ! -f "mkdocs.yml" ]; then
        echo -e "${RED}❌ mkdocs.yml manquant${NC}"
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ mkdocs.yml trouvé${NC}"

        # Validation syntaxe MkDocs
        if command -v mkdocs > /dev/null 2>&1; then
            if ! mkdocs build --strict --verbose > /dev/null 2>&1; then
                echo -e "${RED}❌ mkdocs.yml invalide${NC}"
                errors=$((errors + 1))
            else
                echo -e "${GREEN}✅ Configuration MkDocs valide${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️ mkdocs non installé - validation basique uniquement${NC}"
        fi
    fi
}

# Fonction de validation des scripts
validate_scripts() {
    echo -e "\n${BLUE}🔍 Validation des scripts...${NC}"

    # Scripts critiques
    critical_scripts=(
        "scripts/validate-dockerfiles.sh"
        "scripts/ark-performance-benchmark.py"
        "ark-test-full.sh"
    )

    for script in "${critical_scripts[@]}"; do
        if [ ! -f "$script" ]; then
            echo -e "${RED}❌ $script manquant${NC}"
            errors=$((errors + 1))
        else
            echo -e "${GREEN}✅ $script trouvé${NC}"

            # Vérifier les permissions d'exécution
            if [ ! -x "$script" ]; then
                echo -e "${YELLOW}⚠️ $script : permissions d'exécution manquantes${NC}"
                chmod +x "$script"
                echo -e "${GREEN}✅ Permissions corrigées pour $script${NC}"
            fi
        fi
    done
}

# Validation des workflows GitHub Actions
echo -e "${BLUE}🔍 Validation des workflows GitHub Actions...${NC}"

workflows=(
    ".github/workflows/ci.yml:CI Principal"
    ".github/workflows/deploy.yml:Déploiement principal"
    ".github/workflows/performance-tests.yml:Tests de performance"
    ".github/workflows/docs.yml:Documentation"
    ".github/workflows/e2e.yml:Tests E2E"
)

for workflow_info in "${workflows[@]}"; do
    IFS=':' read -r workflow description <<< "$workflow_info"
    validate_workflow "$workflow" "$description"
done

# Validation des autres composants
validate_dockerfiles
validate_docker_compose
validate_mkdocs
validate_scripts

# Résumé final
echo -e "\n${BLUE}📊 RÉSUMÉ DE LA VALIDATION COMPLÈTE :${NC}"
echo -e "🔍 Workflows GitHub Actions : ${#workflows[@]} vérifiés"
echo -e "🐳 Dockerfiles : 7 vérifiés"
echo -e "📚 MkDocs : 1 vérifié"
echo -e "📜 Scripts : 3 vérifiés"

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "\n${GREEN}✅ VALIDATION COMPLÈTE RÉUSSIE !${NC}"
    echo -e "🎯 Tous les composants sont valides et prêts pour la CI/CD"
    exit 0
elif [ $errors -eq 0 ] && [ $warnings -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️ VALIDATION AVEC AVERTISSEMENTS${NC}"
    echo -e "⚠️ $warnings avertissement(s) détecté(s) mais aucun erreur critique"
    exit 0
else
    echo -e "\n${RED}❌ VALIDATION ÉCHOUÉE${NC}"
    echo -e "❌ $errors erreur(s) critique(s) détectée(s)"
    echo -e "⚠️ $warnings avertissement(s) détecté(s)"
    exit 1
fi
