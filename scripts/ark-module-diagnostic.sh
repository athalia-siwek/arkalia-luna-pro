#!/bin/bash

# 🌕 Arkalia-LUNA Module Diagnostic — Ultra-Pro v3.0
# 📝 Diagnostic complet des modules Arkalia-LUNA
# 👤 Author: Athalia
# 📅 Version: 3.0.0

set -e

# Couleurs Arkalia
ARKALIA_BLUE="\033[38;5;111m"
ARKALIA_GOLD="\033[38;5;220m"
ARKALIA_PINK="\033[38;5;213m"
ARKALIA_GREEN="\033[38;5;82m"
ARKALIA_RED="\033[38;5;196m"
ARKALIA_CYAN="\033[38;5;87m"
RESET="\033[0m"

# Fonction d'affichage stylée
ark_echo() {
    local color=$1
    local emoji=$2
    local message=$3
    echo -e "${color}${emoji} ${message}${RESET}"
}

# Header Arkalia
ark_echo "$ARKALIA_GOLD" "🌕" "Arkalia-LUNA Module Diagnostic — Ultra-Pro v3.0"
echo ""

# Modules attendus
expected_modules=(
    "arkalia_master"
    "assistantia"
    "cognitive_reactor"
    "crossmodule_validator"
    "error_recovery"
    "generative_ai"
    "helloria"
    "monitoring"
    "nyxalia"
    "reflexia"
    "sandozia"
    "security"
    "taskia"
    "utils_enhanced"
    "zeroia"
)

# Vérification de la structure
ark_echo "$ARKALIA_BLUE" "🔍" "Vérification de la structure des modules..."

if [[ ! -d "modules" ]]; then
    ark_echo "$ARKALIA_RED" "❌" "Dossier modules non trouvé"
    exit 1
fi

ark_echo "$ARKALIA_GREEN" "✅" "Dossier modules trouvé"

# Compteurs
total_modules=${#expected_modules[@]}
found_modules=0
missing_modules=()
working_modules=0
broken_modules=0

echo ""

# Vérification de chaque module
ark_echo "$ARKALIA_BLUE" "📋" "Vérification des modules individuels..."

for module in "${expected_modules[@]}"; do
    if [[ -d "modules/$module" ]]; then
        ark_echo "$ARKALIA_GREEN" "✅" "$module"
        ((found_modules++))
        
        # Vérification des fichiers essentiels
        if [[ -f "modules/$module/__init__.py" ]]; then
            ark_echo "$ARKALIA_CYAN" "   📄" "__init__.py présent"
        else
            ark_echo "$ARKALIA_RED" "   ❌" "__init__.py manquant"
        fi
        
        if [[ -f "modules/$module/core.py" ]] || [[ -d "modules/$module/core" ]]; then
            ark_echo "$ARKALIA_CYAN" "   🧠" "Core présent"
            ((working_modules++))
        else
            ark_echo "$ARKALIA_RED" "   ❌" "Core manquant"
            ((broken_modules++))
        fi
        
        # Vérification des tests
        if [[ -d "tests/unit/$module" ]] || [[ -d "tests/integration/$module" ]]; then
            ark_echo "$ARKALIA_CYAN" "   🧪" "Tests présents"
        else
            ark_echo "$ARKALIA_RED" "   ❌" "Tests manquants"
        fi
        
    else
        ark_echo "$ARKALIA_RED" "❌" "$module (manquant)"
        missing_modules+=("$module")
    fi
    echo ""
done

# Rapport de diagnostic
ark_echo "$ARKALIA_GOLD" "📊" "Rapport de diagnostic:"
echo "   • Total attendu: $total_modules modules"
echo "   • Modules trouvés: $found_modules"
echo "   • Modules manquants: $((total_modules - found_modules))"
echo "   • Modules fonctionnels: $working_modules"
echo "   • Modules cassés: $broken_modules"

echo ""

# Modules manquants
if [[ ${#missing_modules[@]} -gt 0 ]]; then
    ark_echo "$ARKALIA_RED" "⚠️" "Modules manquants:"
    for module in "${missing_modules[@]}"; do
        echo "   • $module"
    done
    echo ""
fi

# Vérification Python
ark_echo "$ARKALIA_BLUE" "🐍" "Vérification de l'environnement Python..."

if command -v python &> /dev/null; then
    python_version=$(python --version 2>&1)
    ark_echo "$ARKALIA_GREEN" "✅" "Python: $python_version"
else
    ark_echo "$ARKALIA_RED" "❌" "Python non trouvé"
fi

# Vérification du venv
if [[ -n "$VIRTUAL_ENV" ]]; then
    ark_echo "$ARKALIA_GREEN" "✅" "Venv activé: $VIRTUAL_ENV"
else
    ark_echo "$ARKALIA_RED" "❌" "Venv non activé"
fi

# Vérification des dépendances
ark_echo "$ARKALIA_BLUE" "📦" "Vérification des dépendances..."

if command -v pip &> /dev/null; then
    pip_packages=$(pip list | wc -l)
    ark_echo "$ARKALIA_GREEN" "✅" "$pip_packages packages installés"
else
    ark_echo "$ARKALIA_RED" "❌" "pip non trouvé"
fi

echo ""

# Test d'import des modules
ark_echo "$ARKALIA_BLUE" "🧪" "Test d'import des modules..."

for module in "${expected_modules[@]}"; do
    if [[ -d "modules/$module" ]]; then
        if python -c "import modules.$module" 2>/dev/null; then
            ark_echo "$ARKALIA_GREEN" "✅" "Import $module réussi"
        else
            ark_echo "$ARKALIA_RED" "❌" "Import $module échoué"
        fi
    fi
done

echo ""

# Vérification des scripts
ark_echo "$ARKALIA_BLUE" "🔧" "Vérification des scripts..."

scripts=(
    "ark-start.sh"
    "ark-fix-all.sh"
    "scripts/ark-vscode-reload.sh"
    "scripts/ark-install-extensions.sh"
    "scripts/ark-motivation.sh"
)

for script in "${scripts[@]}"; do
    if [[ -f "$script" ]]; then
        if [[ -x "$script" ]]; then
            ark_echo "$ARKALIA_GREEN" "✅" "$script (exécutable)"
        else
            ark_echo "$ARKALIA_RED" "❌" "$script (non exécutable)"
        fi
    else
        ark_echo "$ARKALIA_RED" "❌" "$script (manquant)"
    fi
done

echo ""

# Recommandations
ark_echo "$ARKALIA_PINK" "💡" "Recommandations:"

if [[ $broken_modules -gt 0 ]]; then
    echo "   • Corrigez les modules cassés"
fi

if [[ ${#missing_modules[@]} -gt 0 ]]; then
    echo "   • Créez les modules manquants"
fi

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "   • Activez le venv: source /Volumes/T7/arkalia-luna-venv/bin/activate"
fi

echo "   • Exécutez les tests: pytest tests/ -v"
echo "   • Vérifiez la configuration: ./scripts/ark-vscode-reload.sh"

echo ""

# Message final
if [[ $broken_modules -eq 0 && ${#missing_modules[@]} -eq 0 ]]; then
    ark_echo "$ARKALIA_GOLD" "🎉" "Tous les modules Arkalia-LUNA sont opérationnels !"
else
    ark_echo "$ARKALIA_RED" "⚠️" "Des problèmes ont été détectés dans les modules"
fi

echo ""
ark_echo "$ARKALIA_GREEN" "🚀" "Diagnostic terminé !"
echo ""

# Motivation finale
if [[ -f "scripts/ark-motivation.sh" ]]; then
    ark_echo "$ARKALIA_GOLD" "🌙" "Boost de motivation..."
    ./scripts/ark-motivation.sh
fi

exit 0 