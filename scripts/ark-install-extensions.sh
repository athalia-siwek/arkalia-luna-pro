#!/bin/bash

# 🌕 Arkalia-LUNA Extensions Installer — Ultra-Pro v3.0
# 📝 Installe les extensions VSCode recommandées pour Arkalia-LUNA
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
ark_echo "$ARKALIA_GOLD" "🌕" "Arkalia-LUNA Extensions Installer — Ultra-Pro v3.0"
echo ""

# Vérification de VSCode
ark_echo "$ARKALIA_BLUE" "🔍" "Vérification de VSCode..."

if ! command -v code &> /dev/null; then
    ark_echo "$ARKALIA_RED" "❌" "VSCode non installé ou non dans le PATH"
    echo ""
    ark_echo "$ARKALIA_BLUE" "💡" "Installez VSCode depuis: https://code.visualstudio.com/"
    exit 1
fi

ark_echo "$ARKALIA_GREEN" "✅" "VSCode détecté"

# Extensions Arkalia-LUNA recommandées
extensions=(
    # 🐍 Python Core
    "ms-python.python"
    "ms-python.black-formatter"
    "ms-python.isort"
    "charliermarsh.ruff"
    
    # 🎨 Thèmes & Icons
    "GitHub.github-vscode-theme"
    "PKief.material-icon-theme"
    "zhuangtongfa.Material-theme"
    
    # 🧠 IA & Productivité
    "GitHub.copilot"
    "GitHub.copilot-chat"
    "ms-vscode.vscode-ai"
    
    # 🔍 Git & GitHub
    "eamodio.gitlens"
    "GitHub.vscode-pull-request-github"
    "GitHub.vscode-github-actions"
    
    # 📊 Monitoring & Debug
    "ms-vscode.vscode-json"
    "redhat.vscode-yaml"
    "ms-azuretools.vscode-docker"
    
    # 🎯 Productivité Avancée
    "esbenp.prettier-vscode"
    "ms-vscode.vscode-eslint"
    
    # 🌕 Arkalia Spécial
    "DavidAnson.vscode-markdownlint"
    "streetsidesoftware.code-spell-checker"
    "ms-vscode.vscode-todo-highlight"
    
    # 📝 Documentation
    "yzhang.markdown-all-in-one"
    "shd101wyy.markdown-preview-enhanced"
    "bierner.markdown-mermaid"
    
    # 🔐 Sécurité
    "ms-azuretools.vscode-docker"
    
    # 🎨 UI/UX
    "ms-vscode.vscode-css-peek"
    "ms-vscode.vscode-html-css-support"
    
    # 🧠 Extensions supplémentaires utiles
    "aaron-bond.better-comments"
    "usernamehw.errorlens"
    "oderwat.indent-rainbow"
    "humao.rest-client"
)

# Extensions déjà installées
ark_echo "$ARKALIA_BLUE" "📋" "Vérification des extensions existantes..."
installed_extensions=$(code --list-extensions 2>/dev/null || echo "")

# Compteurs
total_extensions=${#extensions[@]}
installed_count=0
new_install_count=0
failed_count=0

echo ""

# Installation des extensions
ark_echo "$ARKALIA_BLUE" "🚀" "Installation des extensions Arkalia-LUNA..."

for extension in "${extensions[@]}"; do
    # Extraction du nom d'affichage
    display_name=$(echo "$extension" | sed 's/.*\.//')
    
    if echo "$installed_extensions" | grep -q "^${extension}$"; then
        ark_echo "$ARKALIA_GREEN" "✅" "$display_name (déjà installée)"
        ((installed_count++))
    else
        ark_echo "$ARKALIA_BLUE" "📦" "Installation de $display_name..."
        
        if code --install-extension "$extension" >/dev/null 2>&1; then
            ark_echo "$ARKALIA_GREEN" "✅" "$display_name installée"
            ((new_install_count++))
        else
            ark_echo "$ARKALIA_RED" "❌" "Échec installation $display_name"
            ((failed_count++))
        fi
        
        # Pause pour éviter la surcharge
        sleep 0.5
    fi
done

echo ""

# Rapport d'installation
ark_echo "$ARKALIA_GOLD" "📊" "Rapport d'installation:"
echo "   • Total: $total_extensions extensions"
echo "   • Déjà installées: $installed_count"
echo "   • Nouvelles installations: $new_install_count"
echo "   • Échecs: $failed_count"

echo ""

# Configuration des extensions
ark_echo "$ARKALIA_BLUE" "⚙️" "Configuration des extensions..."

# Configuration du thème
if code --list-extensions | grep -q "GitHub.github-vscode-theme"; then
    ark_echo "$ARKALIA_GREEN" "✅" "Thème GitHub activé"
fi

# Configuration des icônes
if code --list-extensions | grep -q "PKief.material-icon-theme"; then
    ark_echo "$ARKALIA_GREEN" "✅" "Material Icon Theme activé"
fi

# Configuration de GitLens
if code --list-extensions | grep -q "eamodio.gitlens"; then
    ark_echo "$ARKALIA_GREEN" "✅" "GitLens activé"
fi

echo ""

# Recommandations post-installation
ark_echo "$ARKALIA_PINK" "💡" "Recommandations post-installation:"
echo "   • Redémarrez VSCode pour activer toutes les extensions"
echo "   • Configurez GitHub Copilot si vous avez une licence"
echo "   • Personnalisez les thèmes et icônes selon vos préférences"
echo "   • Activez l'auto-save et le formatage automatique"

echo ""

# Script de rechargement
ark_echo "$ARKALIA_BLUE" "🔄" "Rechargement de VSCode..."

if [[ -f "scripts/ark-vscode-reload.sh" ]]; then
    ark_echo "$ARKALIA_GREEN" "✅" "Script de rechargement disponible"
    echo ""
    ark_echo "$ARKALIA_CYAN" "💡" "Exécutez './scripts/ark-vscode-reload.sh' pour recharger VSCode"
else
    ark_echo "$ARKALIA_RED" "❌" "Script de rechargement non trouvé"
fi

echo ""

# Message de succès
if [[ $failed_count -eq 0 ]]; then
    ark_echo "$ARKALIA_GOLD" "🎉" "Installation des extensions Arkalia-LUNA terminée avec succès !"
else
    ark_echo "$ARKALIA_RED" "⚠️" "Installation terminée avec $failed_count échec(s)"
fi

echo ""
ark_echo "$ARKALIA_GREEN" "🚀" "Prêt pour le développement Arkalia-LUNA !"
echo ""

# Motivation finale
if [[ -f "scripts/ark-motivation.sh" ]]; then
    ark_echo "$ARKALIA_GOLD" "🌙" "Boost de motivation..."
    ./scripts/ark-motivation.sh
fi

exit 0 