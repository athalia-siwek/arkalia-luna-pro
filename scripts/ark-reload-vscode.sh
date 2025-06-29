#!/bin/bash

# 🌕 ARKALIA-LUNA — Script de rechargement VSCode
# Version: 3.0-phase1 - Fix configuration errors

echo "🌕 [ARK-RELOAD-VSCODE] Nettoyage et rechargement de la configuration..."

# === Nettoyage du cache VSCode ===
echo "🧹 Nettoyage du cache VSCode..."
rm -rf ~/.vscode/extensions/ms-python.python-*/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.*.so 2>/dev/null || true
rm -rf ~/.vscode/extensions/ms-python.python-*/pythonFiles/lib/python/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.*.pyd 2>/dev/null || true

# === Nettoyage du cache Pyright ===
echo "🧹 Nettoyage du cache Pyright..."
rm -rf ~/.cache/pyright 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true

# === Vérification du venv ===
echo "🔍 Vérification de l'environnement virtuel..."
if [ -f "/Volumes/T7/arkalia-luna-venv/bin/python" ]; then
    echo "✅ Venv trouvé: /Volumes/T7/arkalia-luna-venv/bin/python"
    echo "🐍 Version Python: $(/Volumes/T7/arkalia-luna-venv/bin/python --version)"
else
    echo "❌ Venv non trouvé: /Volumes/T7/arkalia-luna-venv/bin/python"
    echo "💡 Vérifiez que le venv existe ou créez-le avec: python -m venv /Volumes/T7/arkalia-luna-venv"
fi

# === Vérification de la configuration Pyright ===
echo "🔍 Vérification de la configuration Pyright..."
if [ -f "pyrightconfig.json" ]; then
    echo "✅ pyrightconfig.json trouvé"
    # Vérification de la syntaxe JSON
    if python -m json.tool pyrightconfig.json > /dev/null 2>&1; then
        echo "✅ Syntaxe JSON valide"
    else
        echo "❌ Erreur de syntaxe JSON dans pyrightconfig.json"
    fi
else
    echo "❌ pyrightconfig.json manquant"
fi

# === Vérification de la configuration VSCode ===
echo "🔍 Vérification de la configuration VSCode..."
if [ -f ".vscode/settings.json" ]; then
    echo "✅ .vscode/settings.json trouvé"
    # Vérification de la syntaxe JSON
    if python -m json.tool .vscode/settings.json > /dev/null 2>&1; then
        echo "✅ Syntaxe JSON valide"
    else
        echo "❌ Erreur de syntaxe JSON dans .vscode/settings.json"
    fi
else
    echo "❌ .vscode/settings.json manquant"
fi

# === Instructions pour l'utilisateur ===
echo ""
echo "🚀 Instructions pour recharger VSCode :"
echo "1. Fermez VSCode complètement (Cmd+Q)"
echo "2. Rouvrez VSCode dans ce projet"
echo "3. Appuyez sur Cmd+Shift+P et tapez 'Python: Select Interpreter'"
echo "4. Sélectionnez: /Volumes/T7/arkalia-luna-venv/bin/python"
echo "5. Appuyez sur Cmd+Shift+P et tapez 'Developer: Reload Window'"

echo ""
echo "✅ Configuration VSCode Arkalia-LUNA rechargée !"
echo "🌕 Kernel IA ultra-protection active ✅"
