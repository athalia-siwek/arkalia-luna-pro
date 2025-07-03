#!/bin/bash
# 🚀 Script de test rapide de l'API Arkalia-LUNA
# Vérifie que tous les endpoints fonctionnent correctement

set -e

echo "🚀 Test rapide de l'API Arkalia-LUNA..."

# Vérifier que l'API est démarrée
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ API non accessible sur http://localhost:8000"
    echo "💡 Démarrez l'API avec: docker compose up -d arkalia-api"
    exit 1
fi

echo "✅ API accessible"

# Test des endpoints principaux
echo "🔍 Test des endpoints..."

# Test /health
echo "  - /health"
if ! curl -s http://localhost:8000/health | grep -q "ok"; then
    echo "❌ /health échoue"
    exit 1
fi

# Test /zeroia/health
echo "  - /zeroia/health"
if ! curl -s http://localhost:8000/zeroia/health | grep -q "status"; then
    echo "❌ /zeroia/health échoue"
    exit 1
fi

# Test /reflexia/health
echo "  - /reflexia/health"
if ! curl -s http://localhost:8000/reflexia/health | grep -q "status"; then
    echo "❌ /reflexia/health échoue"
    exit 1
fi

# Test /sandozia/health
echo "  - /sandozia/health"
if ! curl -s http://localhost:8000/sandozia/health | grep -q "status"; then
    echo "❌ /sandozia/health échoue"
    exit 1
fi

# Test /decision
echo "  - /decision"
if ! curl -s -X POST http://localhost:8000/decision -H "Content-Type: application/json" -d '{"context": "test"}' | grep -q "decision"; then
    echo "❌ /decision échoue"
    exit 1
fi

# Test /metrics
echo "  - /metrics"
if ! curl -s http://localhost:8000/metrics | grep -q "arkalia"; then
    echo "❌ /metrics échoue"
    exit 1
fi

echo "✅ Tous les endpoints fonctionnent correctement !"
echo "🎉 API Arkalia-LUNA opérationnelle" 