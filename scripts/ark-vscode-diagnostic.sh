#!/bin/bash

# 🌕 ARKALIA-LUNA — Diagnostic VSCode
# Version: 3.0-phase1 - Ultra-Pro Clean

echo "🌕 [ARK-VSCODE-DIAGNOSTIC] Diagnostic complet de l'environnement VSCode..."

# === Vérification de l'environnement ===
echo "🔍 Vérification de l'environnement..."

# Vérification du workspace
if [[ ! -d "/Volumes/T7/devstation/cursor/arkalia-luna-pro" ]]; then
    echo "❌ Erreur : Workspace Arkalia-LUNA non trouvé"
    exit 1
fi

cd /Volumes/T7/devstation/cursor/arkalia-luna-pro

# Vérification de VSCode
if ! command -v code &> /dev/null; then
    echo "❌ Erreur : VSCode non installé ou non dans le PATH"
    exit 1
else
    echo "✅ VSCode installé : $(code --version | head -n1)"
fi

# === Vérification des fichiers de configuration ===
echo "📋 Vérification des fichiers de configuration..."

CONFIG_FILES=(
    ".vscode/settings.json"
    ".vscode/extensions.json"
    ".vscode/tasks.json"
    ".vscode/launch.json"
    ".vscode/devcontainer.json"
    "pyproject.toml"
    ".flake8"
    "pyrightconfig.json"
)

for file in "${CONFIG_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "   ✅ $file"
        
        # Validation JSON pour les fichiers JSON
        if [[ "$file" == *.json ]]; then
            if python3 -m json.tool "$file" > /dev/null 2>&1; then
                echo "      ✅ Syntaxe JSON valide"
            else
                echo "      ❌ Erreur de syntaxe JSON"
            fi
        fi
    else
        echo "   ❌ $file manquant"
    fi
done

# === Vérification des extensions ===
echo "🔌 Vérification des extensions..."

# Extensions requises
REQUIRED_EXTENSIONS=(
    "charliermarsh.ruff"
    "ms-python.black-formatter"
    "ms-python.pyright"
    "ms-python.isort"
)

# Extensions conflictuelles
CONFLICT_EXTENSIONS=(
    "ms-python.flake8"
    "ms-python.pylint"
    "ms-python.vscode-pylance"
)

echo "   Extensions requises :"
for ext in "${REQUIRED_EXTENSIONS[@]}"; do
    if code --list-extensions | grep -q "$ext"; then
        echo "      ✅ $ext installé"
    else
        echo "      ❌ $ext manquant"
    fi
done

echo "   Extensions conflictuelles :"
for ext in "${CONFLICT_EXTENSIONS[@]}"; do
    if code --list-extensions | grep -q "$ext"; then
        echo "      ⚠️  $ext installé (conflit potentiel)"
    else
        echo "      ✅ $ext non installé (correct)"
    fi
done

# === Vérification de l'environnement Python ===
echo "🐍 Vérification de l'environnement Python..."

# Vérification du venv
if [[ -d "/Volumes/T7/arkalia-luna-venv" ]]; then
    echo "   ✅ Venv trouvé : /Volumes/T7/arkalia-luna-venv"
    
    # Vérification de l'interpréteur Python
    if [[ -f "/Volumes/T7/arkalia-luna-venv/bin/python" ]]; then
        echo "   ✅ Interpréteur Python trouvé"
        echo "   📊 Version : $(/Volumes/T7/arkalia-luna-venv/bin/python --version)"
    else
        echo "   ❌ Interpréteur Python manquant"
    fi
else
    echo "   ❌ Venv non trouvé"
fi

# Vérification du PYTHONPATH
echo "   📂 PYTHONPATH : $PYTHONPATH"

# === Vérification des processus VSCode ===
echo "🔄 Vérification des processus VSCode..."

VSCODE_PROCESSES=$(pgrep -f "code" | wc -l)
echo "   📊 Processus VSCode actifs : $VSCODE_PROCESSES"

if [[ $VSCODE_PROCESSES -gt 0 ]]; then
    echo "   📋 Processus VSCode :"
    pgrep -f "code" | head -5 | while read pid; do
        echo "      PID $pid : $(ps -p $pid -o command= | head -1)"
    done
fi

# === Test d'import Python ===
echo "🧪 Test d'import Python..."

# Test avec le venv
if [[ -f "/Volumes/T7/arkalia-luna-venv/bin/python" ]]; then
    echo "   Test avec venv :"
    /Volumes/T7/arkalia-luna-venv/bin/python -c "
import sys
sys.path.insert(0, './modules')
try:
    import core
    print('      ✅ Import modules.core réussi')
except ImportError as e:
    print(f'      ❌ Erreur import: {e}')
"
else
    echo "   ⚠️  Test d'import impossible (venv manquant)"
fi

# === Recommandations ===
echo "💡 Recommandations :"

# Vérification des erreurs détectées
ERRORS_FOUND=0

# Recommandations basées sur les vérifications
if ! code --list-extensions | grep -q "charliermarsh.ruff"; then
    echo "   🔧 Installez l'extension Ruff : code --install-extension charliermarsh.ruff"
    ((ERRORS_FOUND++))
fi

if code --list-extensions | grep -q "ms-python.flake8"; then
    echo "   🚫 Désinstallez Flake8 (conflit avec Ruff) : code --uninstall-extension ms-python.flake8"
    ((ERRORS_FOUND++))
fi

if [[ ! -f ".vscode/settings.json" ]]; then
    echo "   📝 Créez le fichier settings.json"
    ((ERRORS_FOUND++))
fi

# === Résumé ===
echo ""
echo "📊 Résumé du diagnostic :"

if [[ $ERRORS_FOUND -eq 0 ]]; then
    echo "   ✅ Configuration VSCode optimale"
    echo "   🌕 Arkalia-LUNA prêt pour le développement"
else
    echo "   ⚠️  $ERRORS_FOUND problème(s) détecté(s)"
    echo "   🔧 Exécutez les commandes recommandées ci-dessus"
fi

echo ""
echo "🚀 Commandes utiles :"
echo "   • Recharger config : ./scripts/ark-vscode-reload.sh"
echo "   • Installer extensions : ./scripts/ark-install-extensions.sh"
echo "   • Nettoyer système : ./scripts/ark-clean-system.sh" 