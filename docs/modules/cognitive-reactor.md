# Cognitive Reactor — Orchestrateur central

Cognitive Reactor est le module d'orchestration avancée du kernel Arkalia-LUNA. Il fonctionne en mode API HTTP (port 8003) et prend en charge :

- L'orchestration des modules ZeroIA, ReflexIA, Sandozia
- Le redémarrage automatique des modules en cas d'anomalie
- L'analyse de patterns et la génération de prédictions
- L'exposition d'un endpoint API (à venir)

**Entrée/Sortie :**
- Dialogue avec tous les modules critiques
- Peut déclencher des redémarrages, suggestions, alertes

**Cas d'usage :**
- Haute disponibilité
- Résilience système
- Analyse proactive

**API HTTP publique** : http://localhost:8003/ (à compléter selon l'implémentation)
