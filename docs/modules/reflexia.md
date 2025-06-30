# Reflexia — Observateur cognitif réflexif

Reflexia est le module de monitoring cognitif du kernel Arkalia-LUNA. Il fonctionne en mode API HTTP (port 8002) et prend en charge :

- Le monitoring avancé des ressources (CPU, RAM, latence)
- La synchronisation et la validation des décisions ZeroIA
- L'exposition d'un endpoint /metrics compatible Prometheus
- La détection des containers instables

**Entrée/Sortie :**
- Dialogue avec ZeroIA et Sandozia
- Expose une API HTTP (GET /metrics, GET /health)

**Cas d'usage :**
- Supervision temps réel
- Détection d'anomalies
- Intégration Prometheus/Grafana

**API HTTP publique** : http://localhost:8002/metrics
