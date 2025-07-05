#!/usr/bin/env python3
# 🔐 scripts/demo_arkalia_vault.py
# Démonstration d'Arkalia-Vault Enterprise

import sys
from pathlib import Path

from core.ark_logger import ark_logger

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
    ark_logger.info(
        "🔐 === DÉMONSTRATION ARKALIA-VAULT ENTERPRISE ===\n", extra={"module": "scripts"}
    )

    # Créer un vault dans un répertoire temporaire
    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    ark_logger.info(
        "✅ ArkaliaVault initialisé dans:",
        demo_dir / "security" / "vault",
        extra={"module": "scripts"},
    )

    # 1. Stockage de secrets
    ark_logger.info("\n📦 1. STOCKAGE DE SECRETS", extra={"module": "scripts"})
    vault.store_secret(
        "database_url",
        "postgresql://user:pass@localhost/arkalia",
        tags=["production", "database"],
    )
    vault.store_secret(
        "api_key", "ak_prod_12345abcdef", expires_in_days=30, tags=["api", "external"]
    )
    vault.store_secret("jwt_secret", "super_secret_jwt_key_2024", tags=["jwt", "session"])

    ark_logger.info("   ✅ Stocké: database_url", extra={"module": "scripts"})
    ark_logger.info("   ✅ Stocké: api_key (expire dans 30 jours)", extra={"module": "scripts"})
    ark_logger.info("   ✅ Stocké: jwt_secret", extra={"module": "scripts"})

    # 2. Récupération de secrets
    ark_logger.info("\n🔍 2. RÉCUPÉRATION DE SECRETS", extra={"module": "scripts"})
    db_url = vault.retrieve_secret("database_url")
    api_key = vault.retrieve_secret("api_key")

    ark_logger.info(f"   📄 database_url: {db_url[:20]}...", extra={"module": "scripts"})
    ark_logger.info(f"   📄 api_key: {api_key}", extra={"module": "scripts"})

    # 3. Listage des secrets
    ark_logger.info("\n📋 3. LISTAGE DES SECRETS", extra={"module": "scripts"})
    secrets = vault.list_secrets()
    for secret in secrets:
        ark_logger.info(
            f"   📝 {secret.name} - Tags: {secret.tags} - Accès: {secret.access_count}",
            extra={"module": "scripts"},
        )

    # 4. Statistiques du vault
    ark_logger.info("\n📊 4. STATISTIQUES DU VAULT", extra={"module": "scripts"})
    stats = vault.get_vault_stats()
    ark_logger.info(f"   📈 Total secrets: {stats['total_secrets']}", extra={"module": "scripts"})
    ark_logger.info(f"   📈 Secrets actifs: {stats['active_secrets']}", extra={"module": "scripts"})
    ark_logger.info(
        f"   📈 Taille vault: {stats['vault_size_bytes']} bytes", extra={"module": "scripts"}
    )

    return vault


def demo_rotation_manager(vault):
    """Démonstration du gestionnaire de rotation"""
    ark_logger.info("\n🔄 === GESTIONNAIRE DE ROTATION ===\n", extra={"module": "scripts"})

    rotation_manager = RotationManager(vault)

    # 1. Ajouter des politiques de rotation
    ark_logger.info("📋 1. AJOUT DE POLITIQUES DE ROTATION", extra={"module": "scripts"})

    # Politique quotidienne pour JWT
    jwt_policy = create_daily_rotation_policy("jwt_secret")
    rotation_manager.add_policy(jwt_policy)
    ark_logger.info(
        "   ✅ Politique quotidienne ajoutée pour jwt_secret", extra={"module": "scripts"}
    )

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
    ark_logger.info(
        "   ✅ Politique par accès ajoutée pour api_key (max 100 accès)",
        extra={"module": "scripts"},
    )

    # 2. Vérification des rotations nécessaires
    ark_logger.info("\n🔍 2. VÉRIFICATION DES ROTATIONS", extra={"module": "scripts"})
    rotation_check = rotation_manager.bulk_rotation_check()

    for secret_name, (needs_rotation, reason) in rotation_check.items():
        status = "🔄 NÉCESSAIRE" if needs_rotation else "✅ OK"
        ark_logger.info(f"   {status} {secret_name}: {reason}", extra={"module": "scripts"})

    # 3. Forcer une rotation pour la démo
    ark_logger.info("\n🔄 3. ROTATION FORCÉE (DÉMO)", extra={"module": "scripts"})
    result = rotation_manager.rotate_secret("jwt_secret")
    if result:
        ark_logger.info("   ✅ jwt_secret a été tourné avec succès", extra={"module": "scripts"})
        new_value = vault.retrieve_secret("jwt_secret")
        ark_logger.info(f"   🔑 Nouvelle valeur: {new_value[:20]}...", extra={"module": "scripts"})

        # Vérifier les backups
        backups = [s for s in vault.list_secrets() if "backup" in s.name]
        ark_logger.info(f"   📦 {len(backups, extra={"module": "scripts"})} backup(s) créé(s)")

    # 4. Statistiques de rotation
    ark_logger.info("\n📊 4. STATISTIQUES DE ROTATION", extra={"module": "scripts"})
    rotation_stats = rotation_manager.get_rotation_stats()
    ark_logger.info(
        f"   📈 Politiques actives: {rotation_stats['total_policies']}", extra={"module": "scripts"}
    )
    ark_logger.info(
        f"   📈 Rotations effectuées: {rotation_stats['total_rotations']}",
        extra={"module": "scripts"},
    )
    ark_logger.info(
        f"   📈 Distribution: {rotation_stats['strategy_distribution']}",
        extra={"module": "scripts"},
    )

    return rotation_manager


def demo_token_manager(vault):
    """Démonstration du gestionnaire de tokens"""
    ark_logger.info("\n🎫 === GESTIONNAIRE DE TOKENS ===\n", extra={"module": "scripts"})

    token_manager = TokenManager(vault)

    # 1. Génération de tokens de session
    ark_logger.info("🎟️ 1. GÉNÉRATION DE TOKENS DE SESSION", extra={"module": "scripts"})

    session_id, session_token = create_session_token(
        token_manager=token_manager,
        user_id="athalia",
        client_ip="192.168.1.100",
        user_agent="Mozilla/5.0 (Arkalia Browser)",
        permissions=["read", "write", "admin"],
        session_duration_hours=24,
    )

    ark_logger.info(f"   ✅ Token de session créé: {session_id}", extra={"module": "scripts"})
    ark_logger.info(f"   🎫 Token: {session_token[:50]}...", extra={"module": "scripts"})

    # 2. Génération de clés API
    ark_logger.info("\n🔑 2. GÉNÉRATION DE CLÉS API", extra={"module": "scripts"})

    api_id, api_token = token_manager.generate_token(
        token_type=TokenType.API_KEY,
        service_id="reflexia_service",
        permissions=["api_read", "api_write"],
        max_usage_count=1000,
    )

    ark_logger.info(f"   ✅ Clé API créée: {api_id}", extra={"module": "scripts"})
    ark_logger.info(f"   🔑 Clé: {api_token}", extra={"module": "scripts"})

    # 3. Validation de tokens
    ark_logger.info("\n✅ 3. VALIDATION DE TOKENS", extra={"module": "scripts"})

    # Valider le token de session
    is_valid, metadata, reason = token_manager.validate_token(session_token)
    ark_logger.info(
        f"   🎫 Session token valide: {is_valid} - {reason}", extra={"module": "scripts"}
    )
    if metadata:
        ark_logger.info(
            f"      👤 Utilisateur: {metadata.associated_user}", extra={"module": "scripts"}
        )
        ark_logger.info(
            f"      🔐 Permissions: {metadata.permissions}", extra={"module": "scripts"}
        )
        ark_logger.info(
            f"      📊 Utilisations: {metadata.usage_count}", extra={"module": "scripts"}
        )

    # Valider la clé API
    is_valid, metadata, reason = token_manager.validate_token(
        api_token, required_permissions=["api_read"]
    )
    ark_logger.info(f"   🔑 API key valide: {is_valid} - {reason}", extra={"module": "scripts"})

    # 4. Statistiques des tokens
    ark_logger.info("\n📊 4. STATISTIQUES DES TOKENS", extra={"module": "scripts"})
    token_stats = token_manager.get_token_stats()
    ark_logger.info(
        f"   📈 Total tokens: {token_stats['total_tokens']}", extra={"module": "scripts"}
    )
    ark_logger.info(
        f"   📈 Tokens actifs: {token_stats['active_tokens']}", extra={"module": "scripts"}
    )
    ark_logger.info(f"   📈 Par type: {token_stats['by_type']}", extra={"module": "scripts"})
    ark_logger.info(
        f"   📈 Usage total: {token_stats['usage_stats']['total_usage']}",
        extra={"module": "scripts"},
    )

    # 5. Révocation de token
    ark_logger.info("\n🚫 5. RÉVOCATION DE TOKEN", extra={"module": "scripts"})
    revoke_result = token_manager.revoke_token(api_id, "Démo de révocation")
    ark_logger.info(f"   ✅ Token révoqué: {revoke_result}", extra={"module": "scripts"})

    # Vérifier que le token révoqué n'est plus valide
    is_valid, _, reason = token_manager.validate_token(api_token)
    ark_logger.info(
        f"   🚫 Token après révocation: {is_valid} - {reason}", extra={"module": "scripts"}
    )

    return token_manager


def demo_vault_integrity():
    """Démonstration de la validation d'intégrité"""
    ark_logger.info("\n🛡️ === VALIDATION D'INTÉGRITÉ ===\n", extra={"module": "scripts"})

    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    ark_logger.info("🔍 1. VALIDATION D'INTÉGRITÉ COMPLÈTE", extra={"module": "scripts"})
    try:
        integrity_result = vault.validate_vault_integrity()
        ark_logger.info(
            f"   ✅ Intégrité du vault: {integrity_result}", extra={"module": "scripts"}
        )
    except Exception as e:
        ark_logger.info(f"   ❌ Violation d'intégrité: {e}", extra={"module": "scripts"})

    ark_logger.info("\n🔐 2. ROTATION DE LA CLÉ MAÎTRE", extra={"module": "scripts"})
    try:
        new_key = vault.rotate_master_key()
        ark_logger.info(
            f"   ✅ Clé maître tournée: {len(new_key, extra={"module": "scripts"})} bytes"
        )

        # Re-valider l'intégrité après rotation
        integrity_result = vault.validate_vault_integrity()
        ark_logger.info(
            f"   ✅ Intégrité après rotation: {integrity_result}", extra={"module": "scripts"}
        )

    except Exception as e:
        ark_logger.info(f"   ❌ Erreur de rotation: {e}", extra={"module": "scripts"})


def demo_migration_env():
    """Démonstration de la migration depuis .env"""
    ark_logger.info("\n🚀 === MIGRATION DEPUIS .ENV ===\n", extra={"module": "scripts"})

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
    ark_logger.info("📁 Fichier .env de démo créé", extra={"module": "scripts"})

    # Migration vers le vault
    demo_dir = Path("./demo_vault")
    vault = ArkaliaVault(base_dir=demo_dir)

    from modules.security.crypto import migrate_from_env_file

    migrated_count = migrate_from_env_file(demo_env, vault, backup_env=True)

    ark_logger.info(f"✅ {migrated_count} secrets migrés depuis .env", extra={"module": "scripts"})

    # Vérifier les secrets migrés
    ark_logger.info("\n📋 SECRETS MIGRÉS:", extra={"module": "scripts"})
    migrated_secrets = [s for s in vault.list_secrets() if "migrated_from_env" in s.tags]
    for secret in migrated_secrets:
        value = vault.retrieve_secret(secret.name)
        ark_logger.info(f"   📝 {secret.name}: {value}", extra={"module": "scripts"})

    # Nettoyer
    demo_env.unlink()
    ark_logger.info("\n🧹 Fichier .env de démo supprimé", extra={"module": "scripts"})


def main():
    """Fonction principale de démonstration"""
    try:
        # Démonstrations séquentielles
        vault = demo_basic_vault_operations()
        rotation_manager = demo_rotation_manager(vault)
        token_manager = demo_token_manager(vault)
        demo_vault_integrity()
        demo_migration_env()

        ark_logger.info("\n🎉 === DÉMONSTRATION TERMINÉE ===", extra={"module": "scripts"})
        ark_logger.info(
            "✅ Arkalia-Vault Enterprise fonctionne parfaitement !", extra={"module": "scripts"}
        )

        # Statistiques finales
        ark_logger.info("\n📊 STATISTIQUES FINALES:", extra={"module": "scripts"})
        final_stats = vault.get_vault_stats()
        ark_logger.info(
            f"   📈 Total secrets: {final_stats['total_secrets']}", extra={"module": "scripts"}
        )
        ark_logger.info(
            f"   📈 Secrets actifs: {final_stats['active_secrets']}", extra={"module": "scripts"}
        )

        token_stats = token_manager.get_token_stats()
        ark_logger.info(
            f"   🎫 Total tokens: {token_stats['total_tokens']}", extra={"module": "scripts"}
        )
        ark_logger.info(
            f"   🎫 Tokens actifs: {token_stats['active_tokens']}", extra={"module": "scripts"}
        )

        rotation_stats = rotation_manager.get_rotation_stats()
        ark_logger.info(
            f"   🔄 Politiques rotation: {rotation_stats['total_policies']}",
            extra={"module": "scripts"},
        )

        ark_logger.info(
            "\n📁 Données sauvegardées dans: ./demo_vault/security/vault/",
            extra={"module": "scripts"},
        )

    except Exception as e:
        ark_logger.info(f"❌ Erreur lors de la démonstration: {e}", extra={"module": "scripts"})
        import traceback

        traceback.print_exc()

    finally:
        ark_logger.info("\n💡 Pour nettoyer: rm -rf ./demo_vault/", extra={"module": "scripts"})


if __name__ == "__main__":
    main()
