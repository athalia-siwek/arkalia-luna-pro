# Tests de Chaos

Ce dossier regroupe les tests de chaos engineering.

- **But** : Valider la résilience du système face à des pannes simulées (CPU, réseau, fichiers, etc).
- **Organisation** : Un fichier par type de chaos.
- **Exécution** : `pytest tests/chaos/`

## Conventions

- Fichiers : `test_*.py`
- Markers : `@pytest.mark.chaos`
- Scénarios documentés dans des fichiers `.yaml` si besoin

## Bonnes pratiques

- Exécuter ces tests dans un environnement isolé
- Documenter chaque scénario de chaos
- Nettoyer l'état du système après chaque test

## Structure

- `filesystem/` : tests de corruption et résilience fichiers
- `system/` : tests de charge CPU/mémoire
- `network/` : tests de coupure réseau/DNS
- `state/` : tests de corruption d'état
- `common.py` : utilitaires et classes partagées

## Exécution rapide

```bash
pytest tests/chaos/filesystem/
pytest tests/chaos/system/
pytest tests/chaos/network/
pytest tests/chaos/state/
```

## Marqueurs

- `@pytest.mark.chaos` : tests de chaos
- `@pytest.mark.slow` : tests longs

## Exemple de test

```python
import pytest
from tests.chaos.common import ChaosTestConfig, ChaosTester

class TestFileSystemChaos:
    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_atomic_write_resilience(self):
        """Test résilience écriture atomique sous charge"""
        # ...
```

## Conseil

Lance les tests de chaos en mode dédié (nightly/cron) pour ne pas ralentir la CI classique.
