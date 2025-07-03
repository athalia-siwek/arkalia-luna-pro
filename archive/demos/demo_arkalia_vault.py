#!/usr/bin/env python3
# 🔐 scripts/demo_arkalia_vault.py
# Démonstration d'Arkalia-Vault Enterprise

import sys
from pathlib import Path

# Ajouter le projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# flake8: noqa: E402
from modules.security.crypto import (
    ArkaliaVault,
    RotationManager,
    RotationStrategy,
    TokenManager,
    TokenType,
    create_daily_rotation_policy,
    create_session_token,
)


def demo_basic_vault_operations():
    """Démonstration des opérations de base du vault"""
    print("🔐 === DÉMONSTRATION ARKALIA-VAULT ENTERPRISE ===\n")

    # Créer un vault dans un répertoire temporaire
    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    print("✅ ArkaliaVault initialisé dans:", demo_dir / "security" / "vault")

    # 1. Stockage de secrets
    print("\n📦 1. STOCKAGE DE SECRETS")
    vault.store_secret(
        "database_url",
        "postgresql://user:pass@localhost/arkalia",
        tags=["production", "database"],
    )
    vault.store_secret(
        "api_key", "ak_prod_12345abcdef", expires_in_days=30, tags=["api", "external"]
    )
    vault.store_secret("jwt_secret", "super_secret_jwt_key_2024", tags=["jwt", "session"])

    print("   ✅ Stocké: database_url")
    print("   ✅ Stocké: api_key (expire dans 30 jours)")
    print("   ✅ Stocké: jwt_secret")

    # 2. Récupération de secrets
    print("\n🔍 2. RÉCUPÉRATION DE SECRETS")
    db_url = vault.retrieve_secret("database_url")
    api_key = vault.retrieve_secret("api_key")

    print(f"   📄 database_url: {db_url[:20]}...")
    print(f"   📄 api_key: {api_key}")

    # 3. Listage des secrets
    print("\n📋 3. LISTAGE DES SECRETS")
    secrets = vault.list_secrets()
    for secret in secrets:
        print(f"   📝 {secret.name} - Tags: {secret.tags} - Accès: {secret.access_count}")

    # 4. Statistiques du vault
    print("\n📊 4. STATISTIQUES DU VAULT")
    stats = vault.get_vault_stats()
    print(f"   📈 Total secrets: {stats['total_secrets']}")
    print(f"   📈 Secrets actifs: {stats['active_secrets']}")
    print(f"   📈 Taille vault: {stats['vault_size_bytes']} bytes")

    return vault


def demo_rotation_manager(vault):
    """Démonstration du gestionnaire de rotation"""
    print("\n🔄 === GESTIONNAIRE DE ROTATION ===\n")

    rotation_manager = RotationManager(vault)

    # 1. Ajouter des politiques de rotation
    print("📋 1. AJOUT DE POLITIQUES DE ROTATION")

    # Politique quotidienne pour JWT
    jwt_policy = create_daily_rotation_policy("jwt_secret")
    rotation_manager.add_policy(jwt_policy)
    print("   ✅ Politique quotidienne ajoutée pour jwt_secret")

    # Politique basée sur l'accès pour API key
    from modules.security.crypto import RotationPolicy

    api_policy = RotationPolicy(
        name="api_key",
        strategy=RotationStrategy.ACCESS_COUNT,
        max_access_count=100,
        auto_generate=True,
        generation_pattern="api_key",
    )
    rotation_manager.add_policy(api_policy)
    print("   ✅ Politique par accès ajoutée pour api_key (max 100 accès)")

    # 2. Vérification des rotations nécessaires
    print("\n🔍 2. VÉRIFICATION DES ROTATIONS")
    rotation_check = rotation_manager.bulk_rotation_check()

    for secret_name, (needs_rotation, reason) in rotation_check.items():
        status = "🔄 NÉCESSAIRE" if needs_rotation else "✅ OK"
        print(f"   {status} {secret_name}: {reason}")

    # 3. Forcer une rotation pour la démo
    print("\n🔄 3. ROTATION FORCÉE (DÉMO)")
    result = rotation_manager.rotate_secret("jwt_secret")
    if result:
        print("   ✅ jwt_secret a été tourné avec succès")
        new_value = vault.retrieve_secret("jwt_secret")
        print(f"   🔑 Nouvelle valeur: {new_value[:20]}...")

        # Vérifier les backups
        backups = [s for s in vault.list_secrets() if "backup" in s.name]
        print(f"   📦 {len(backups)} backup(s) créé(s)")

    # 4. Statistiques de rotation
    print("\n📊 4. STATISTIQUES DE ROTATION")
    rotation_stats = rotation_manager.get_rotation_stats()
    print(f"   📈 Politiques actives: {rotation_stats['total_policies']}")
    print(f"   📈 Rotations effectuées: {rotation_stats['total_rotations']}")
    print(f"   📈 Distribution: {rotation_stats['strategy_distribution']}")

    return rotation_manager


def demo_token_manager(vault):
    """Démonstration du gestionnaire de tokens"""
    print("\n🎫 === GESTIONNAIRE DE TOKENS ===\n")

    token_manager = TokenManager(vault)

    # 1. Génération de tokens de session
    print("🎟️ 1. GÉNÉRATION DE TOKENS DE SESSION")

    session_id, session_token = create_session_token(
        token_manager=token_manager,
        user_id="athalia",
        client_ip="192.168.1.100",
        user_agent="Mozilla/5.0 (Arkalia Browser)",
        permissions=["read", "write", "admin"],
        session_duration_hours=24,
    )

    print(f"   ✅ Token de session créé: {session_id}")
    print(f"   🎫 Token: {session_token[:50]}...")

    # 2. Génération de clés API
    print("\n🔑 2. GÉNÉRATION DE CLÉS API")

    api_id, api_token = token_manager.generate_token(
        token_type=TokenType.API_KEY,
        service_id="reflexia_service",
        permissions=["api_read", "api_write"],
        max_usage_count=1000,
    )

    print(f"   ✅ Clé API créée: {api_id}")
    print(f"   🔑 Clé: {api_token}")

    # 3. Validation de tokens
    print("\n✅ 3. VALIDATION DE TOKENS")

    # Valider le token de session
    is_valid, metadata, reason = token_manager.validate_token(session_token)
    print(f"   🎫 Session token valide: {is_valid} - {reason}")
    if metadata:
        print(f"      👤 Utilisateur: {metadata.associated_user}")
        print(f"      🔐 Permissions: {metadata.permissions}")
        print(f"      📊 Utilisations: {metadata.usage_count}")

    # Valider la clé API
    is_valid, metadata, reason = token_manager.validate_token(
        api_token, required_permissions=["api_read"]
    )
    print(f"   🔑 API key valide: {is_valid} - {reason}")

    # 4. Statistiques des tokens
    print("\n📊 4. STATISTIQUES DES TOKENS")
    token_stats = token_manager.get_token_stats()
    print(f"   📈 Total tokens: {token_stats['total_tokens']}")
    print(f"   📈 Tokens actifs: {token_stats['active_tokens']}")
    print(f"   📈 Par type: {token_stats['by_type']}")
    print(f"   📈 Usage total: {token_stats['usage_stats']['total_usage']}")

    # 5. Révocation de token
    print("\n🚫 5. RÉVOCATION DE TOKEN")
    revoke_result = token_manager.revoke_token(api_id, "Démo de révocation")
    print(f"   ✅ Token révoqué: {revoke_result}")

    # Vérifier que le token révoqué n'est plus valide
    is_valid, _, reason = token_manager.validate_token(api_token)
    print(f"   🚫 Token après révocation: {is_valid} - {reason}")

    return token_manager


def demo_vault_integrity():
    """Démonstration de la validation d'intégrité"""
    print("\n🛡️ === VALIDATION D'INTÉGRITÉ ===\n")

    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    print("🔍 1. VALIDATION D'INTÉGRITÉ COMPLÈTE")
    try:
        integrity_result = vault.validate_vault_integrity()
        print(f"   ✅ Intégrité du vault: {integrity_result}")
    except Exception as e:
        print(f"   ❌ Violation d'intégrité: {e}")

    print("\n🔐 2. ROTATION DE LA CLÉ MAÎTRE")
    try:
        new_key = vault.rotate_master_key()
        print(f"   ✅ Clé maître tournée: {len(new_key)} bytes")

        # Re-valider l'intégrité après rotation
        integrity_result = vault.validate_vault_integrity()
        print(f"   ✅ Intégrité après rotation: {integrity_result}")

    except Exception as e:
        print(f"   ❌ Erreur de rotation: {e}")


def demo_migration_env():
    """Démonstration de la migration depuis .env"""
    print("\n🚀 === MIGRATION DEPUIS .ENV ===\n")

    # Créer un fichier .env de démo
    demo_env = Path("./demo.env")
    env_content = """# Fichier .env de démonstration
DATABASE_URL=postgresql://user:secret@localhost/arkalia_prod
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=ultra_secret_key_for_production
API_TOKEN=bearer_token_12345
DEBUG=false
"""
    demo_env.write_text(env_content)
    print("📁 Fichier .env de démo créé")

    # Migration vers le vault
    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    from modules.security.crypto import migrate_from_env_file

    migrated_count = migrate_from_env_file(demo_env, vault, backup_env=True)

    print(f"✅ {migrated_count} secrets migrés depuis .env")

    # Vérifier les secrets migrés
    print("\n📋 SECRETS MIGRÉS:")
    migrated_secrets = [s for s in vault.list_secrets() if "migrated_from_env" in s.tags]
    for secret in migrated_secrets:
        value = vault.retrieve_secret(secret.name)
        print(f"   📝 {secret.name}: {value}")

    # Nettoyer
    demo_env.unlink()
    print("\n🧹 Fichier .env de démo supprimé")


def main():
    """Fonction principale de démonstration"""
    try:
        # Démonstrations séquentielles
        vault = demo_basic_vault_operations()
        rotation_manager = demo_rotation_manager(vault)
        token_manager = demo_token_manager(vault)
        demo_vault_integrity()
        demo_migration_env()

        print("\n🎉 === DÉMONSTRATION TERMINÉE ===")
        print("✅ Arkalia-Vault Enterprise fonctionne parfaitement !")

        # Statistiques finales
        print("\n📊 STATISTIQUES FINALES:")
        final_stats = vault.get_vault_stats()
        print(f"   📈 Total secrets: {final_stats['total_secrets']}")
        print(f"   📈 Secrets actifs: {final_stats['active_secrets']}")

        token_stats = token_manager.get_token_stats()
        print(f"   🎫 Total tokens: {token_stats['total_tokens']}")
        print(f"   🎫 Tokens actifs: {token_stats['active_tokens']}")

        rotation_stats = rotation_manager.get_rotation_stats()
        print(f"   🔄 Politiques rotation: {rotation_stats['total_policies']}")

        print("\n📁 Données sauvegardées dans: ./demo_vault/security/vault/")

    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback

        traceback.print_exc()

    finally:
        print("\n💡 Pour nettoyer: rm -rf ./demo_vault/")


if __name__ == "__main__":
    main()
