#!/bin/bash

# 🌕 Arkalia-LUNA VSCode Reload Script — Ultra-Pro v3.0
# 📝 Recharge la configuration VSCode avec style Arkalia
# 👤 Author: Athalia
# 📅 Version: 3.0.0

set -e

# Couleurs Arkalia
ARKALIA_BLUE="\033[38;5;111m"
ARKALIA_GOLD="\033[38;5;220m"
ARKALIA_PINK="\033[38;5;213m"
ARKALIA_GREEN="\033[38;5;82m"
ARKALIA_RED="\033[38;5;196m"
RESET="\033[0m"

# Fonction d'affichage stylée
ark_echo() {
    local color=$1
    local emoji=$2
    local message=$3
    echo -e "${color}${emoji} ${message}${RESET}"
}

# Header Arkalia
ark_echo "$ARKALIA_GOLD" "🌕" "Arkalia-LUNA VSCode Reload — Ultra-Pro v3.0"
echo ""

# Vérification de l'environnement
ark_echo "$ARKALIA_BLUE" "🔍" "Vérification de l'environnement..."

if [[ ! -d ".vscode" ]]; then
    ark_echo "$ARKALIA_RED" "❌" "Dossier .vscode non trouvé"
    exit 1
fi

if ! command -v code &> /dev/null; then
    ark_echo "$ARKALIA_RED" "❌" "VSCode non installé ou non dans le PATH"
    exit 1
fi

ark_echo "$ARKALIA_GREEN" "✅" "Environnement vérifié"

# Nettoyage des fichiers cachés macOS
ark_echo "$ARKALIA_BLUE" "🧹" "Nettoyage des fichiers cachés macOS..."
find .vscode -name "._*" -delete 2>/dev/null || true
find .vscode -name ".DS_Store" -delete 2>/dev/null || true
ark_echo "$ARKALIA_GREEN" "✅" "Fichiers cachés nettoyés"

# Vérification des fichiers de configuration
ark_echo "$ARKALIA_BLUE" "📋" "Vérification des fichiers de configuration..."

config_files=("settings.json" "tasks.json" "extensions.json" "launch.json" "arkalia-snippets.code-snippets")
missing_files=()

for file in "${config_files[@]}"; do
    if [[ -f ".vscode/$file" ]]; then
        ark_echo "$ARKALIA_GREEN" "✅" "$file"
    else
        ark_echo "$ARKALIA_RED" "❌" "$file (manquant)"
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo ""
    ark_echo "$ARKALIA_RED" "⚠️" "Fichiers manquants détectés:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    ark_echo "$ARKALIA_BLUE" "💡" "Exécutez './scripts/ark-fix-vscode-config.sh' pour les créer"
fi

# Rechargement de VSCode
ark_echo "$ARKALIA_BLUE" "🔄" "Rechargement de VSCode..."

# Fermeture de VSCode s'il est ouvert
if pgrep -x "Code" > /dev/null; then
    ark_echo "$ARKALIA_BLUE" "🔄" "Fermeture de VSCode..."
    pkill -x "Code" || true
    sleep 2
fi

# Ouverture avec la nouvelle configuration
ark_echo "$ARKALIA_BLUE" "🚀" "Ouverture de VSCode avec la configuration Arkalia..."
code . --disable-extensions --force-disable-user-env

# Attente pour le chargement
sleep 3

# Réactivation des extensions
ark_echo "$ARKALIA_BLUE" "🔌" "Réactivation des extensions..."
code . --enable-proposed-api

# Vérification finale
ark_echo "$ARKALIA_BLUE" "🔍" "Vérification finale..."

# Test de la configuration Python
if [[ -f ".vscode/settings.json" ]]; then
    if grep -q "python.defaultInterpreterPath" .vscode/settings.json; then
        ark_echo "$ARKALIA_GREEN" "✅" "Configuration Python détectée"
    else
        ark_echo "$ARKALIA_RED" "❌" "Configuration Python manquante"
    fi
fi

# Test des tâches
if [[ -f ".vscode/tasks.json" ]]; then
    task_count=$(grep -c '"label":' .vscode/tasks.json || echo "0")
    ark_echo "$ARKALIA_GREEN" "✅" "$task_count tâches Arkalia configurées"
fi

# Test des snippets
if [[ -f ".vscode/arkalia-snippets.code-snippets" ]]; then
    snippet_count=$(grep -c '"prefix":' .vscode/arkalia-snippets.code-snippets || echo "0")
    ark_echo "$ARKALIA_GREEN" "✅" "$snippet_count snippets Arkalia disponibles"
fi

# Message de succès
echo ""
ark_echo "$ARKALIA_GOLD" "🎉" "VSCode Arkalia-LUNA rechargé avec succès !"
echo ""
ark_echo "$ARKALIA_PINK" "💡" "Raccourcis utiles:"
echo "   • Cmd+Shift+P → 'Tasks: Run Task' → Sélectionnez une tâche Arkalia"
echo "   • Cmd+Shift+P → 'Developer: Reload Window' → Recharge complet"
echo "   • Cmd+, → Paramètres → Vérifiez la configuration Python"
echo ""
ark_echo "$ARKALIA_GREEN" "🚀" "Prêt pour le développement Arkalia-LUNA !"
echo ""

# Motivation finale
if [[ -f "scripts/ark-motivation.sh" ]]; then
    ark_echo "$ARKALIA_GOLD" "🌙" "Boost de motivation..."
    ./scripts/ark-motivation.sh
fi

exit 0 