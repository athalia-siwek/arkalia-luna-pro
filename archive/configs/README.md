# 🗄️ archive/configs/

Ce dossier contient toutes les **configurations archivées** du projet Arkalia Luna Pro.

## 📋 Liste des fichiers archivés

- `docker-compose.fixed.yml`
- `docker-compose.master.yml`
- `docker-compose.optimized.yml`
- `docker-compose.prod.yml`
- `docker-compose.simple.yml`
- `Dockerfile.assistantia`
- `Dockerfile.cognitive-reactor`
- `Dockerfile.generative-ai`
- `Dockerfile.master`
- `Dockerfile.reflexia`
- `Dockerfile.sandozia`
- `Dockerfile.zeroia`
- `pytest-chaos.ini`
- `pytest-integration.ini`
- `pytest-performance.ini`
- `pytest-security.ini`

## 🔄 Restauration d'une config

Pour restaurer un fichier archivé à la racine ou dans le dossier voulu :

```bash
./restore_config.sh <nom_du_fichier>
```

Exemple :
```bash
./restore_config.sh pytest-integration.ini
```

---
**Aucune config n'est supprimée, tout est archivé ici pour traçabilité et restauration rapide.**
