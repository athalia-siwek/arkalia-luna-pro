#!/bin/bash
# 🛡️ ark-secret-check — Détecteur de secrets sensibles (PAT, tokens, clés)

echo "🔐 [ark-secret-check] Lancement de l'analyse de sécurité des fichiers..."

# PAT GitHub
grep -rIn --color=always 'ghp_[A-Za-z0-9]\{36,\}' . && echo "❌ Token PAT détecté !" && exit 1

# Clés privées (simples détections)
grep -rIn --color=always '-----BEGIN PRIVATE KEY-----' . && echo "❌ Clé privée détectée !" && exit 1
grep -rIn --color=always '-----BEGIN RSA PRIVATE KEY-----' . && echo "❌ Clé RSA détectée !" && exit 1

# Secrets génériques
grep -rIn --color=always 'AKIA[0-9A-Z]{16}' . && echo "❌ Clé AWS détectée !" && exit 1

# Vérifie les .env
find . -type f -name "*.env" | while read -r file; do
  echo "🧐 Analyse de $file..."
  grep -iE '(token|secret|password|key)=' "$file" && echo "⚠️  Potentiel secret dans $file" && exit 1
done

echo "✅ Aucun secret critique détecté."
exit 0
