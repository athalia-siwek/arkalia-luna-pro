# 💾 Backup & Recovery — Arkalia-LUNA

![Backup](https://img.shields.io/badge/backup-automated-green)
![Recovery](https://img.shields.io/badge/recovery-tested-blue)
![Integrity](https://img.shields.io/badge/integrity-verified-orange)

**Stratégie complète de sauvegarde et récupération pour Arkalia-LUNA** — Protection des données critiques, snapshots automatisés et récupération d'urgence.

---

## 🎯 Stratégie de Sauvegarde Arkalia-LUNA

### **Architecture 3-2-1 Adaptée IA**
- **3** copies des données critiques
- **2** supports de stockage différents
- **1** copie hors site (cloud chiffré)
- **+** Validation automatique intégrité

### **Données Critiques Identifiées**

| Type de Données | Localisation | Criticité | Fréquence Backup |
|------------------|--------------|-----------|------------------|
| **États IA** | `modules/*/state/*.toml` | 🔴 CRITIQUE | **Temps réel** |
| **Configurations** | `config/*.toml`, `.env` | 🔴 CRITIQUE | **6h** |
| **Modèles LLM** | `/var/lib/ollama/models/` | 🟧 ÉLEVÉE | **24h** |
| **Logs Audit** | `logs/*.log` | 🟧 ÉLEVÉE | **12h** |
| **Code Source** | Git repository | 🟨 MOYENNE | **Push temps réel** |
| **Base de données** | States JSON/TOML | 🔴 CRITIQUE | **1h** |

---

## 🔄 Snapshots Automatisés

### **Snapshot États IA (Temps Réel)**
```bash
#!/bin/bash
# scripts/ark_realtime_snapshot.sh

SNAPSHOT_DIR="/backup/realtime"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Fonction snapshot atomique
create_atomic_snapshot() {
    local source="$1"
    local dest="$2"
    local temp_file="${dest}.tmp.${TIMESTAMP}"

    # Copie atomique avec validation
    cp "$source" "$temp_file" && \
    python -c "import toml; toml.load('$temp_file')" && \
    mv "$temp_file" "$dest" && \
    echo "✅ Snapshot: $(basename $dest)"
}

# Snapshot tous états critiques
for state_file in modules/*/state/*.toml state/*.toml global_state/*.toml; do
    if [ -f "$state_file" ]; then
        relative_path=${state_file#*/}
        backup_path="$SNAPSHOT_DIR/$relative_path.$TIMESTAMP"
        mkdir -p "$(dirname "$backup_path")"
        create_atomic_snapshot "$state_file" "$backup_path"
    fi
done

# Nettoyage snapshots > 7 jours
find "$SNAPSHOT_DIR" -name "*.toml.*" -mtime +7 -delete

echo "📸 Snapshot temps réel terminé: $TIMESTAMP"
```

### **Snapshot Système Complet (Journalier)**
```bash
#!/bin/bash
# scripts/ark_full_backup.sh

BACKUP_ROOT="/backup/daily"
DATE=$(date +%Y%m%d)
BACKUP_DIR="$BACKUP_ROOT/arkalia_$DATE"

echo "🏗️ BACKUP COMPLET ARKALIA-LUNA - $DATE"

# Création répertoire horodaté
mkdir -p "$BACKUP_DIR"

# 1. États et configurations (priorité max)
echo "💾 Sauvegarde états IA..."
tar -czf "$BACKUP_DIR/arkalia_states_$DATE.tar.gz" \
    modules/*/state/ \
    state/ \
    global_state/ \
    config/ \
    .env 2>/dev/null

# 2. Logs système et audit
echo "📋 Sauvegarde logs..."
tar -czf "$BACKUP_DIR/arkalia_logs_$DATE.tar.gz" \
    logs/ \
    modules/*/logs/ 2>/dev/null

# 3. Modèles LLM (si modifiés)
if [ -d "/var/lib/ollama/models" ]; then
    echo "🧠 Sauvegarde modèles LLM..."
    tar -czf "$BACKUP_DIR/ollama_models_$DATE.tar.gz" \
        -C /var/lib/ollama models/ 2>/dev/null
fi

# 4. Configurations Docker et scripts
echo "🐳 Sauvegarde infrastructure..."
tar -czf "$BACKUP_DIR/arkalia_infra_$DATE.tar.gz" \
    docker-compose.yml \
    Dockerfile* \
    scripts/ \
    .github/ \
    requirements.txt \
    pyproject.toml 2>/dev/null

# 5. Génération checksums intégrité
cd "$BACKUP_DIR"
sha256sum *.tar.gz > "checksums_$DATE.sha256"

# 6. Métadonnées backup
cat > "backup_manifest_$DATE.json" << EOF
{
    "backup_date": "$(date -Iseconds)",
    "arkalia_version": "$(cat version.toml | grep current_version | cut -d'"' -f2)",
    "backup_size_mb": $(du -sm "$BACKUP_DIR" | cut -f1),
    "files_count": $(find "$BACKUP_DIR" -type f | wc -l),
    "git_commit": "$(git rev-parse HEAD)",
    "host": "$(hostname)",
    "backup_type": "full_daily"
}
EOF

echo "✅ Backup complet terminé: $BACKUP_DIR"

# Nettoyage backups > 30 jours
find "$BACKUP_ROOT" -name "arkalia_*" -type d -mtime +30 -exec rm -rf {} \;
```

---

## 🔐 Chiffrement et Sécurité

### **Chiffrement Backups Sensibles**
```bash
#!/bin/bash
# scripts/ark_encrypted_backup.sh

GPG_RECIPIENT="arkalia-backup@system.local"
ENCRYPTED_DIR="/backup/encrypted"

# Fonction chiffrement GPG
encrypt_backup() {
    local source="$1"
    local encrypted_name="${source##*/}.gpg"

    gpg --trust-model always --encrypt \
        --recipient "$GPG_RECIPIENT" \
        --output "$ENCRYPTED_DIR/$encrypted_name" \
        "$source"

    # Vérification intégrité
    if gpg --decrypt "$ENCRYPTED_DIR/$encrypted_name" | sha256sum > /tmp/verify.sha; then
        echo "✅ Backup chiffré validé: $encrypted_name"
    else
        echo "❌ Erreur chiffrement: $encrypted_name"
        return 1
    fi
}

# Chiffrement états critiques
for backup in /backup/daily/arkalia_*/arkalia_states_*.tar.gz; do
    if [ -f "$backup" ]; then
        encrypt_backup "$backup"
    fi
done
```

### **Stockage Sécurisé Distant**
```bash
#!/bin/bash
# scripts/ark_remote_sync.sh

REMOTE_BACKUP="user@backup-server:/secure/arkalia/"
ENCRYPTED_DIR="/backup/encrypted"

# Synchronisation chiffrée vers site distant
rsync -avz --progress --delete \
    --exclude="*.tmp" \
    "$ENCRYPTED_DIR/" \
    "$REMOTE_BACKUP"

echo "🌐 Synchronisation distante terminée"
```

---

## 🚀 Procédures de Récupération

### **Récupération État IA Critique**
```bash
#!/bin/bash
# scripts/ark_emergency_restore.sh

restore_critical_state() {
    local module="$1"
    local backup_date="$2"

    echo "🔄 RESTAURATION URGENTE: $module"

    # Arrêt service concerné
    docker stop "$module" 2>/dev/null

    # Sauvegarde état actuel (corrompu)
    cp "modules/$module/state/${module}_state.toml" \
       "/tmp/${module}_corrupted_$(date +%s).toml" 2>/dev/null

    # Recherche backup le plus récent
    if [ -n "$backup_date" ]; then
        BACKUP_FILE="/backup/daily/arkalia_$backup_date/arkalia_states_$backup_date.tar.gz"
    else
        BACKUP_FILE=$(find /backup/daily -name "arkalia_states_*.tar.gz" | sort -r | head -1)
    fi

    if [ ! -f "$BACKUP_FILE" ]; then
        echo "❌ Aucun backup trouvé"
        return 1
    fi

    # Extraction et restauration
    cd /tmp
    tar -xzf "$BACKUP_FILE" "modules/$module/state/" 2>/dev/null

    if [ -f "/tmp/modules/$module/state/${module}_state.toml" ]; then
        # Validation avant restauration
        python -c "import toml; toml.load('/tmp/modules/$module/state/${module}_state.toml')" || {
            echo "❌ Backup TOML invalide"
            return 1
        }

        # Restauration effective
        cp "/tmp/modules/$module/state/${module}_state.toml" \
           "modules/$module/state/${module}_state.toml"

        # Redémarrage service
        docker start "$module"
        sleep 5

        echo "✅ $module restauré depuis: $(basename $BACKUP_FILE)"
        docker logs "$module" --tail 10
    else
        echo "❌ État $module non trouvé dans backup"
        return 1
    fi
}

# Usage: restore_critical_state zeroia 20241225
restore_critical_state "$1" "$2"
```

### **Récupération Complète Système**
```bash
#!/bin/bash
# scripts/ark_disaster_recovery.sh

echo "💥 RÉCUPÉRATION COMPLÈTE ARKALIA-LUNA"

# 1. Validation prérequis
if [ ! -d "/backup/daily" ]; then
    echo "❌ Répertoire backup inaccessible"
    exit 1
fi

# 2. Arrêt tous services
docker-compose down --remove-orphans

# 3. Récupération backup le plus récent
LATEST_BACKUP=$(find /backup/daily -name "arkalia_*" -type d | sort -r | head -1)
echo "📦 Restauration depuis: $LATEST_BACKUP"

# 4. Extraction états critiques
cd "$LATEST_BACKUP"
tar -xzf arkalia_states_*.tar.gz -C /
tar -xzf arkalia_infra_*.tar.gz -C /

# 5. Validation intégrité
echo "🔍 Validation intégrité..."
sha256sum -c checksums_*.sha256 || {
    echo "❌ Checksums invalides"
    exit 1
}

# 6. Reconstruction environnement
echo "🏗️ Reconstruction conteneurs..."
docker-compose build --no-cache

# 7. Tests prédémarrage
echo "🧪 Tests validation..."
python -m pytest tests/unit/test_state_writer.py -v

# 8. Redémarrage graduel
echo "🚀 Redémarrage graduel..."
docker-compose up -d reflexia
sleep 10
docker-compose up -d zeroia helloria
sleep 10
docker-compose up -d assistantia

# 9. Validation finale
echo "✅ Validation post-récupération..."
sleep 30
curl -f http://localhost:8000/status || echo "⚠️ API non disponible"
docker ps --format "table {.Names}\t{.Status}"

echo "🎯 Récupération terminée - monitoring requis"
```

---

## 💽 Récupération Perte Disque Totale

### **Procédure Disaster Recovery**
```bash
#!/bin/bash
# scripts/ark_disk_recovery.sh

echo "💽 RÉCUPÉRATION PERTE DISQUE TOTAL"

# 1. Installation environnement minimal
install_base_system() {
    # Installation Docker, Git, Python
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh

    apt-get update && apt-get install -y git python3 python3-pip
    pip3 install docker-compose
}

# 2. Clonage repository
clone_arkalia() {
    git clone https://github.com/arkalia-luna-system/arkalia-luna-pro.git
    cd arkalia-luna-pro
    git checkout main
}

# 3. Récupération backups distants
restore_from_remote() {
    # Téléchargement backups chiffrés depuis site distant
    rsync -avz backup-server:/secure/arkalia/encrypted/ /backup/encrypted/

    # Déchiffrement backup le plus récent
    LATEST_ENCRYPTED=$(find /backup/encrypted -name "arkalia_states_*.tar.gz.gpg" | sort -r | head -1)
    gpg --decrypt "$LATEST_ENCRYPTED" > /tmp/arkalia_states_latest.tar.gz

    # Extraction dans structure projet
    tar -xzf /tmp/arkalia_states_latest.tar.gz
}

# 4. Validation et démarrage
validate_and_start() {
    # Tests intégrité basiques
    ./scripts/ark-sec-check.sh --basic-validation

    # Construction environnement
    docker-compose build

    # Démarrage contrôlé
    docker-compose up -d

    echo "✅ Récupération perte disque terminée"
    echo "⚠️ Surveillance accrue recommandée pendant 48h"
}

# Exécution complète
install_base_system
clone_arkalia
restore_from_remote
validate_and_start
```

---

## 🧪 Tests de Récupération

### **Tests Automatisés Backup/Restore**
```python
# tests/backup/test_backup_recovery.py

import pytest
import os
import subprocess
import tempfile
import toml

class TestBackupRecovery:

    def test_state_backup_integrity(self):
        """Teste l'intégrité des backups d'états"""
        # Création état test
        test_state = {
            "decision": {
                "last_decision": "test_backup",
                "confidence_score": 0.9,
                "timestamp": "2024-01-01T12:00:00"
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml') as f:
            toml.dump(test_state, f)
            f.flush()

            # Test backup
            result = subprocess.run(['scripts/ark_realtime_snapshot.sh'],
                                  capture_output=True, text=True)
            assert result.returncode == 0

    def test_emergency_restore(self):
        """Teste la restauration d'urgence"""
        # Simulation corruption fichier
        corrupt_file = "modules/zeroia/state/zeroia_state.toml"

        # Sauvegarde original
        with open(corrupt_file, 'r') as f:
            original = f.read()

        # Corruption simulation
        with open(corrupt_file, 'w') as f:
            f.write("invalid toml content {[}")

        # Test restauration
        result = subprocess.run(['scripts/ark_emergency_restore.sh', 'zeroia'],
                              capture_output=True, text=True)

        # Validation restoration
        assert result.returncode == 0
        assert toml.load(corrupt_file) is not None

    def test_full_backup_cycle(self):
        """Teste cycle complet backup/restore"""
        # Lancement backup complet
        result = subprocess.run(['scripts/ark_full_backup.sh'],
                              capture_output=True, text=True)
        assert result.returncode == 0

        # Vérification fichiers générés
        backup_files = subprocess.run(['find', '/backup/daily', '-name', '*.tar.gz'],
                                    capture_output=True, text=True)
        assert len(backup_files.stdout.strip().split('\n')) >= 3
```

### **Simulation Panne Disque**
```bash
#!/bin/bash
# tests/chaos/disk_failure_simulation.sh

echo "💽 SIMULATION PANNE DISQUE (Test contrôlé)"

# 1. Sauvegarde état actuel
backup_current_state() {
    cp -r modules/*/state /tmp/test_backup_states/
    cp -r state /tmp/test_backup_global/
}

# 2. Simulation "perte" données
simulate_disk_loss() {
    # Renommage temporaire (simulation perte)
    mv modules/zeroia/state modules/zeroia/state.hidden
    mv state state.hidden

    echo "🚨 Simulation: Données état perdues"
}

# 3. Test procédure récupération
test_recovery() {
    ./scripts/ark_disaster_recovery.sh --test-mode
}

# 4. Restauration état test
restore_test_state() {
    mv modules/zeroia/state.hidden modules/zeroia/state
    mv state.hidden state

    echo "✅ État test restauré"
}

# Exécution test complet
backup_current_state
simulate_disk_loss
test_recovery
restore_test_state
```

---

## 📊 Monitoring et Alertes Backup

### **Métriques Prometheus Backup**
```python
# modules/monitoring/backup_metrics.py

from prometheus_client import Gauge, Counter, Histogram

# Métriques backup
backup_last_success = Gauge('arkalia_backup_last_success_timestamp',
                           'Timestamp du dernier backup réussi')

backup_size_bytes = Gauge('arkalia_backup_size_bytes',
                         'Taille backup en bytes', ['type'])

backup_duration_seconds = Histogram('arkalia_backup_duration_seconds',
                                  'Durée backup en secondes', ['type'])

backup_failures_total = Counter('arkalia_backup_failures_total',
                               'Nombre échecs backup', ['type', 'reason'])

def update_backup_metrics():
    """Met à jour métriques backup"""
    import os
    import time

    # Dernière réussite backup
    latest_backup = max([os.path.getmtime(f) for f in
                        glob.glob('/backup/daily/arkalia_*')])
    backup_last_success.set(latest_backup)

    # Taille backups par type
    for backup_type in ['states', 'logs', 'models', 'infra']:
        pattern = f'/backup/daily/*/arkalia_{backup_type}_*.tar.gz'
        files = glob.glob(pattern)
        if files:
            total_size = sum([os.path.getsize(f) for f in files])
            backup_size_bytes.labels(type=backup_type).set(total_size)
```

### **Alertes Grafana Backup**
```yaml
# configs/grafana_backup_alerts.yml

groups:
  - name: arkalia_backup_alerts
    rules:
      - alert: BackupTooOld
        expr: time() - arkalia_backup_last_success_timestamp > 86400
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "Backup Arkalia-LUNA trop ancien"
                          description: "Dernier backup réussi il y a {value}s"

      - alert: BackupSizeAnomalous
        expr: increase(arkalia_backup_size_bytes[1d]) > 1.5 * increase(arkalia_backup_size_bytes[7d]) / 7
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Taille backup anormale"
          description: "Augmentation backup inhabituelle détectée"

      - alert: BackupFailures
        expr: increase(arkalia_backup_failures_total[1h]) > 0
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "Échecs backup détectés"
          description: "{{ $value }} échecs backup dernière heure"
```

---

## 📋 Checklist Maintenance Backup

### **Quotidienne**
- [ ] ✅ Vérification exécution backups automatiques
- [ ] ✅ Contrôle taille et nombre fichiers backup
- [ ] ✅ Validation checksums backup journalier
- [ ] ✅ Test accessibilité stockage distant

### **Hebdomadaire**
- [ ] ✅ Test restauration état sur environnement test
- [ ] ✅ Nettoyage backups expirés (> 30 jours)
- [ ] ✅ Vérification capacité stockage disponible
- [ ] ✅ Audit logs backup et erreurs

### **Mensuelle**
- [ ] ✅ Test récupération complète environnement test
- [ ] ✅ Rotation clés chiffrement GPG
- [ ] ✅ Validation intégrité backups distants
- [ ] ✅ Exercice disaster recovery complet

---

## 📞 Contacts Backup d'Urgence

### **Récupération Critique**
- 🚨 **Backup Emergency** : backup-emergency@arkalia-luna.system
- 💾 **Storage Admin** : storage@arkalia-luna.system
- 🔐 **Crypto Key Manager** : keymaster@arkalia-luna.system

### **Fournisseurs Externes**
- ☁️ **Cloud Backup Provider** : support@backup-provider.com
- 🏢 **Data Center Contact** : noc@datacenter.com
- 🛠️ **Hardware Support** : hardware@vendor.com

---

*Documentation maintenue par Arkalia-LUNA Backup Team — Tests récupération validés mensuellement*
*💾 "Sauvegarde continue, récupération instantanée" — Arkalia Backup Doctrine*
