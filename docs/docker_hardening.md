# Docker Hardening

## Objectif
Réduire la surface d'attaque même en local en appliquant des règles de sécurité strictes aux conteneurs Docker.

## Règles de sécurité appliquées

### 1. read_only: true
Cette option monte le système de fichiers du conteneur en lecture seule, empêchant toute modification non autorisée des fichiers système.

### 2. restart: on-failure
Cette option redémarre automatiquement le conteneur uniquement en cas d'échec, ce qui améliore la résilience tout en évitant les redémarrages inutiles.

### 3. cap_drop: ALL
Cette option supprime toutes les capacités Linux du conteneur, réduisant ainsi les privilèges et limitant les actions que le conteneur peut effectuer, ce qui diminue la surface d'attaque potentielle.

# 🛡️ Sécurisation Docker (Docker Hardening)

Version : Arkalia v2.5.x+

## 1. `docker-compose.yml`

Ajoute les options suivantes à chaque service :

```yaml
services:
  assistantia:
    read_only: true
    restart: on-failure
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL


      2. Réseau
	•	Utilise un réseau interne :

    networks:
  arknet:
    driver: bridge

    3. Dossiers montés
	•	Ne monte jamais un dossier sensible en rw :

    volumes:
  - ./state:/app/state:ro

  4. Éviter les privilèges root
	•	Dans ton Dockerfile :

    RUN useradd -m arkuser
USER arkuser

5. Outils de scan sécurité

docker scan arkalia-api
