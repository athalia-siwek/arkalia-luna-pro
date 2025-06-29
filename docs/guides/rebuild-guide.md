# Rebuild & Reconstruction

Documentation pour la reconstruction et le rebuild d'Arkalia-LUNA.

## Guide de Reconstruction

Pour consulter le guide complet de reconstruction, voir [Guide Rebuild](rebuild-guide.md).

## Procédures Rapides

### Rebuild Complet
```bash
# Nettoyage complet
ark-clean

# Reconstruction
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Rebuild Documentation
```bash
# Documentation locale
ark-docs-local

# Déploiement documentation
ark-docs
```

[📖 Guide Complet →](rebuild-guide.md)
