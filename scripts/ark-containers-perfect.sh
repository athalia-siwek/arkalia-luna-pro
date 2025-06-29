#!/bin/bash
# 🚀 Arkalia-LUNA - Gestion Parfaite des Conteneurs Optimisés

# === COMMANDES PRINCIPALES ===

# 🚀 Démarrer tous les conteneurs optimisés
ark-start-optimized() {
    echo "🚀 Démarrage des conteneurs Arkalia optimisés..."
    ark-clean
    docker-compose -f docker-compose.simple.yml up -d
    sleep 5
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep optimized
}

# 🛑 Arrêter tous les conteneurs optimisés
ark-stop-optimized() {
    echo "🛑 Arrêt des conteneurs Arkalia optimisés..."
    docker-compose -f docker-compose.simple.yml down
}

# 🔄 Redémarrer avec rebuild complet
ark-rebuild-optimized() {
    echo "🔄 Reconstruction complète des conteneurs optimisés..."
    ark-clean
    docker-compose -f docker-compose.simple.yml down
    docker system prune -f
    docker-compose -f docker-compose.simple.yml up -d --build --force-recreate
}

# 📊 Statut détaillé des conteneurs optimisés
ark-status-optimized() {
    echo "📊 Statut des conteneurs Arkalia optimisés :"
    echo ""
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(optimized|NAMES)"
    echo ""
    echo "💾 Tailles des images :"
    docker images | grep arkalia-luna-pro | awk '{print $1 "\t" $7 $8}' | head -6
    echo ""
    echo "🔌 Tests de connectivité :"
    if curl -f http://localhost:8000 2>/dev/null; then
        echo "✅ API principale accessible (port 8000)"
    else
        echo "⚠️ API principale non accessible"
    fi
    
    if curl -f http://localhost:8001 2>/dev/null; then
        echo "✅ AssistantIA accessible (port 8001)"
    else
        echo "⚠️ AssistantIA non accessible"
    fi
}

# 🔍 Logs des conteneurs optimisés
ark-logs-optimized() {
    local service=${1:-"arkalia-api"}
    echo "🔍 Logs du service $service-optimized :"
    docker logs ${service}-optimized --tail=50 -f
}

# 🧠 Démarrer seulement les IA cognitives
ark-start-cognitive() {
    echo "🧠 Démarrage des modules IA cognitifs..."
    docker-compose -f docker-compose.simple.yml up -d zeroia sandozia cognitive-reactor
    docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(zeroia|sandozia|cognitive)"
}

# === EXPORT DES FONCTIONS ===
export -f ark-start-optimized
export -f ark-stop-optimized  
export -f ark-rebuild-optimized
export -f ark-status-optimized
export -f ark-logs-optimized
export -f ark-start-cognitive

echo "🎉 Fonctions de gestion optimisée chargées !"
echo "📝 Commandes disponibles :"
echo "   ark-start-optimized     - Démarre tous les conteneurs"
echo "   ark-stop-optimized      - Arrête tous les conteneurs"
echo "   ark-rebuild-optimized   - Reconstruit tout"
echo "   ark-status-optimized    - Statut détaillé"
echo "   ark-logs-optimized      - Voir les logs"
echo "   ark-start-cognitive     - IA cognitives seulement" 