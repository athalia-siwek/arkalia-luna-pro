# 🔐 Tests Arkalia-Vault — Arkalia-LUNA

## Objectif
Tests unitaires pour le système de gestion sécurisée des secrets Arkalia-Vault Enterprise.

## Structure
- `test_vault.py` : Tests pour la classe ArkaliaVault (stockage, récupération, expiration, rotation)
- `test_rotation_manager.py` : Tests pour le gestionnaire de rotation des secrets
- `test_token_manager.py` : Tests pour la gestion des tokens d'accès
- `test_migration.py` : Tests pour les fonctions de migration depuis d'autres systèmes

## Exécution rapide
```bash
pytest tests/unit/security/arkalia_vault/
pytest tests/unit/security/arkalia_vault/test_vault.py
pytest tests/unit/security/arkalia_vault/test_rotation_manager.py
```

## Marqueurs
- `@pytest.mark.security` : Tests de sécurité
- `@pytest.mark.slow` : Tests longs (rotation, migration)

## Bonnes pratiques
- Utiliser des répertoires temporaires pour les tests
- Nettoyer automatiquement les secrets créés
- Tester les cas d'erreur et d'expiration
- Valider l'intégrité des secrets après rotation

## Exemple de test
```python
import pytest
from modules.security.crypto import ArkaliaVault

class TestArkaliaVault:
    @pytest.fixture
    def vault(self, temp_vault_dir):
        return ArkaliaVault(base_dir=temp_vault_dir)

    def test_store_and_retrieve_secret(self, vault):
        result = vault.store_secret("test_secret", "secret_value")
        assert result is True
        retrieved = vault.retrieve_secret("test_secret")
        assert retrieved == "secret_value"
```

## Conseil
Ces tests valident la sécurité et la robustesse du système de gestion des secrets critique. 