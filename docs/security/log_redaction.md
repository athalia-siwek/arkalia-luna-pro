# 🧹 Politique de Redaction des Logs - Arkalia-LUNA

## Vue d'ensemble

La politique de redaction des logs d'Arkalia-LUNA garantit la sécurité et la conformité RGPD en supprimant automatiquement les données sensibles des fichiers de logs.

## 🎯 Objectifs de Sécurité

- **Protection des données sensibles** : Mots de passe, tokens, clés API
- **Conformité RGPD** : Suppression automatique des IPs privées
- **Audit de sécurité** : Traçabilité des actions de nettoyage
- **Performance** : Rotation et archivage intelligent

## 🔍 Données Sensibles Détectées

### 1. 🔐 Authentification

```regex
# Mots de passe
password["':\s]*["']\w+["']\s*

# Tokens
token["':\s]*["']\w+["']\s*

# Clés API
api_key["':\s]*["']\w+["']\s*

# Bearer tokens
Bearer [A-Za-z0-9\-._~+/]+=*
```

### 2. 🌐 Informations Réseau

```regex
# IPs privées classe A (10.x.x.x)
\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b

# IPs privées classe B (172.16-31.x.x)
\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b

# IPs privées classe C (192.168.x.x)
\b192\.168\.\d{1,3}\.\d{1,3}\b
```

### 3. 🔑 Clés Cryptographiques

```regex
# Clés SSH
ssh-rsa [A-Za-z0-9+/=]+

# Clés ed25519
ssh-ed25519 [A-Za-z0-9+/=]+

# Signatures GPG
-----BEGIN PGP SIGNATURE-----.*-----END PGP SIGNATURE-----
```

## 🛠️ Configuration Log Scrubber

### Fichier de Configuration

```json
{
  "log_directories": [
    "logs/",
    "modules/*/logs/",
    "infrastructure/monitoring/loki/",
    "infrastructure/monitoring/prometheus/"
  ],
  "max_log_age_days": 30,
  "max_log_size_mb": 100,
  "sensitive_patterns": [
    "password[\"':\\s]*[\"']\\w+[\"']\\s*",
    "token[\"':\\s]*[\"']\\w+[\"']\\s*",
    "api_key[\"':\\s]*[\"']\\w+[\"']\\s*",
    "\\b192\\.168\\.\\d{1,3}\\.\\d{1,3}\\b",
    "\\b10\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b",
    "\\b172\\.(1[6-9]|2[0-9]|3[0-1])\\.\\d{1,3}\\.\\d{1,3}\\b",
    "Bearer [A-Za-z0-9\\-._~+/]+=*",
    "ssh-rsa [A-Za-z0-9+/=]+"
  ],
  "archive_directory": "logs/archives/",
  "dry_run": false
}
```

### Variables d'Environnement

```bash
# Configuration personnalisée
export ARKALIA_LOG_SCRUBBER_CONFIG="./config/log_scrubber.json"

# Mode dry-run global
export ARKALIA_SCRUBBER_DRY_RUN="true"

# Niveau de verbose
export ARKALIA_SCRUBBER_VERBOSE="true"
```

## 🕐 Automatisation et Scheduling

### Configuration Cron

```bash
# Nettoyage quotidien à 02:00
0 2 * * * cd /path/to/arkalia && python scripts/log_scrubber.py

# Nettoyage hebdomadaire complet (dimanche 03:00)
0 3 * * 0 cd /path/to/arkalia && python scripts/log_scrubber.py --verbose

# Purge archives anciennes (1er du mois 04:00)
0 4 1 * * find logs/archives/ -name '*.gz' -mtime +90 -delete
```

### Installation Automatique

```bash
# Configuration cron automatique
bash scripts/setup_log_scrubber_cron.sh

# Vérification status
crontab -l | grep "Arkalia-LUNA"
```

## 📊 Métriques de Nettoyage

### Statistiques Collectées

```python
stats = {
    "files_processed": 156,
    "sensitive_data_removed": 23,
    "bytes_saved": 2457600,  # ~2.4MB
    "archives_created": 12,
    "errors": []
}
```

### Rapport de Nettoyage

```
🧹 [LOG SCRUBBER] Nettoyage terminé - 2025-06-27 18:45:00

📊 STATISTIQUES:
   📁 Fichiers traités: 156
   🔒 Données sensibles supprimées: 23
   💾 Espace libéré: 2.4MB
   📦 Archives créées: 12
   ⏱️ Durée: 3.2s

🎯 TYPES DE DONNÉES NETTOYÉES:
   • Mots de passe: 5
   • Tokens Bearer: 8
   • IPs privées: 10

📁 ROTATION DES LOGS:
   • Logs > 100MB: 3 fichiers archivés
   • Logs > 30 jours: 9 fichiers supprimés

✅ Nettoyage réussi sans erreurs
```

## 🔒 Politique de Rétention

### Règles de Conservation

| Type de Log | Durée de Rétention | Action |
|-------------|-------------------|---------|
| **Logs système** | 30 jours | Suppression |
| **Logs audit** | 90 jours | Archive compressée |
| **Logs erreur** | 60 jours | Archive + alerte |
| **Métriques** | 365 jours | Agrégation |

### Archivage Intelligent

```bash
# Compression automatique
gzip logs/old_file.log > logs/archives/old_file_20250627.log.gz

# Vérification intégrité
gzip -t logs/archives/*.gz

# Purge automatique (>90 jours)
find logs/archives/ -name "*.gz" -mtime +90 -delete
```

## 🔍 Exemples de Redaction

### Avant Redaction

```log
2025-06-27 18:30:00 [INFO] User login: password="secret123" from 192.168.1.100
2025-06-27 18:31:00 [AUTH] API call with token="Bearer eyJ0eXAiOiJKV1QiLCJhbGc"
2025-06-27 18:32:00 [SSH] Key exchange: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB...
```

### Après Redaction

```log
2025-06-27 18:30:00 [INFO] User login: password="[REDACTED]" from [IP_REDACTED]
2025-06-27 18:31:00 [AUTH] API call with token="[REDACTED]"
2025-06-27 18:32:00 [SSH] Key exchange: [SSH_KEY_REDACTED]
```

## 🛡️ Sécurité du Processus

### Protection des Backups

```bash
# Permissions restrictives
chmod 600 logs/archives/*.gz

# Chiffrement optionnel
gpg --cipher-algo AES256 --compress-algo 1 --symmetric logs/sensitive.log
```

### Audit Trail

```log
2025-06-27 18:45:00 [SCRUBBER] Started log cleaning process
2025-06-27 18:45:01 [SCRUBBER] Pattern match: password in logs/app.log:42
2025-06-27 18:45:01 [SCRUBBER] Redacted: logs/app.log line 42
2025-06-27 18:45:02 [SCRUBBER] Archive created: logs/archives/app_20250627.log.gz
2025-06-27 18:45:03 [SCRUBBER] Process completed successfully
```

## 🚀 Utilisation

### Mode Manuel

```bash
# Nettoyage standard
python scripts/log_scrubber.py

# Mode dry-run (test)
python scripts/log_scrubber.py --dry-run

# Mode verbose
python scripts/log_scrubber.py --verbose

# Configuration personnalisée
python scripts/log_scrubber.py --config config/custom_scrubber.json
```

### Mode Automatique

```bash
# Installation cron
bash scripts/setup_log_scrubber_cron.sh

# Vérification logs cron
tail -f logs/cron_scrubber.log

# Status du service
systemctl status crond  # Linux
launchctl list | grep cron  # macOS
```

## 📋 Conformité RGPD

### Droits des Utilisateurs

- **Droit à l'effacement** : Suppression automatique après 30 jours
- **Droit à la portabilité** : Exports disponibles avant suppression
- **Droit d'accès** : Logs d'audit disponibles sur demande

### Documentation de Conformité

- **Registre des traitements** : Mis à jour automatiquement
- **Analyse d'impact** : Intégrée au processus de nettoyage
- **Mesures techniques** : Chiffrement + contrôle d'accès

## ⚠️ Bonnes Pratiques

1. **Test en dry-run** avant première utilisation
2. **Backup critique** avant nettoyage de masse
3. **Monitoring des erreurs** de redaction
4. **Validation périodique** des patterns de détection
5. **Formation équipe** sur les procédures de conformité

## 🔧 Dépannage

### Erreurs Communes

```bash
# Permissions insuffisantes
chmod +x scripts/log_scrubber.py

# Python introuvable
which python3
export PATH="/usr/bin:$PATH"

# Logs corrompus
python scripts/log_scrubber.py --skip-corrupted
```

### Récupération d'Urgence

```bash
# Restauration depuis archive
gunzip logs/archives/critical_20250627.log.gz

# Bypass temporaire du nettoyage
export ARKALIA_SCRUBBER_DRY_RUN="true"

# Reset configuration
rm -f config/log_scrubber.json
```
