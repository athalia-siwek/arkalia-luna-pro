#!/bin/bash

# 🌕 Arkalia-LUNA Pro - Script de rechargement du thème sombre
# Version: 3.0-phase1 - Thème Noir & Bleu Doux

echo "🌕 [ARKALIA] Rechargement du thème sombre..."

# Vérifier si VSCode est ouvert
if pgrep -x "Code" > /dev/null; then
    echo "✅ VSCode détecté, rechargement en cours..."
    
    # Recharger la fenêtre VSCode
    code --command workbench.action.reloadWindow
    
    echo "🎨 Thème sombre appliqué !"
    echo "   - Fond noir doux (#1e1e1e)"
    echo "   - Texte bleu doux (#87CEEB)"
    echo "   - Sélections bleues (#2a4a6a)"
    echo "   - Surlignage de ligne (#2a2a2a)"
    echo ""
    echo "💡 Si les changements ne sont pas visibles immédiatement :"
    echo "   1. Appuyez sur Cmd+Shift+P"
    echo "   2. Tapez 'Developer: Reload Window'"
    echo "   3. Ou redémarrez VSCode"
else
    echo "⚠️  VSCode n'est pas ouvert"
    echo "   Ouvrez VSCode et relancez ce script"
fi

echo ""
echo "🌕 [ARKALIA] Configuration du thème terminée !" 