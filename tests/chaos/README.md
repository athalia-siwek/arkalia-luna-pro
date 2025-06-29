# 🌀 Tests de Chaos — Arkalia-LUNA

## Objectif
Valider la résilience du système face à des conditions extrêmes (corruption, charge CPU, réseau instable, etc.)

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

## Bonnes pratiques
- Toujours restaurer l'état après chaque test
- Utiliser les fixtures et helpers du dossier `common`
- Découper chaque scénario dans un fichier dédié
- Documenter chaque test avec une docstring claire

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
