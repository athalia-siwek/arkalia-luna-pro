#!/bin/bash

echo "🧹 Nettoyage des fichiers invisibles macOS..."
find ./docs -type f -name '._*' -exec rm -v {} \;
find . -name '.DS_Store' -delete
echo "✅ Nettoyage terminé."
