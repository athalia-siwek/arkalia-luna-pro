# 🧪 Suite de Tests de Chaos - Arkalia-LUNA

## Vue d'ensemble

La suite de tests de chaos d'Arkalia-LUNA valide la résilience du système face à des pannes, corruptions et attaques simulées.

## 🎯 Objectifs

- **Validation de résilience** : Le système survit aux pannes
- **Tests de récupération** : Capacité de récupération automatique
- **Détection de points faibles** : Identification des vulnérabilités
- **Métriques de robustesse** : Score de résilience quantifié

## 🔧 Installation

```bash
# Lancement rapide
python scripts/chaos_test.py

# Mode simulation (recommandé pour premiers tests)
python scripts/chaos_test.py --dry-run

# Test de durée spécifique
python scripts/chaos_test.py --duration 120

# Scénario spécifique
python scripts/chaos_test.py --scenario config
```

## 🌪️ Scénarios de Chaos

### 1. 💥 Corruption de Configuration

**Objectif :** Tester la robustesse face aux fichiers de config corrompus

```bash
python scripts/chaos_test.py --scenario config
```

**Cibles :**
- `config/settings.toml`
- `config/monitoring_config.toml`
- `modules/zeroia/state/zeroia_state.toml`
- `modules/reflexia/state/reflexia_state.toml`

**Méthodes de corruption :**
- Injection de caractères invalides
- Troncature de fichier
- Syntaxe TOML malformée

### 2. 🗑️ Suppression de Fichiers Critiques

**Objectif :** Validation de la récupération face à la perte de fichiers

```bash
python scripts/chaos_test.py --scenario files
```

**Cibles :**
- `modules/zeroia/core.py`
- `modules/reflexia/core.py`
- `modules/assistantia/core.py`
- `version.toml`

### 3. 🧠 Surcharge Mémoire

**Objectif :** Test de comportement sous stress mémoire

```bash
python scripts/chaos_test.py --scenario memory
```

**Méthode :**
- Allocation progressive de chunks 50MB
- Maximum 1GB alloué
- Libération progressive

### 4. 🌐 Simulation d'Erreurs Réseau

**Objectif :** Validation de la résilience réseau

```bash
python scripts/chaos_test.py --scenario network
```

**Services testés :**
- API Arkalia (:8000)
- Prometheus (:9090)
- Grafana (:3000)
- Ollama (:11434)

### 5. 🤖 Corruption État ZeroIA

**Objectif :** Test spécifique corruption IA décisionnelle

```bash
python scripts/chaos_test.py --scenario zeroia
```

**Méthodes d'injection :**
- `cpu = "CHAOS_ERROR"`
- `ram = -999.9`
- `decision = "malformed_decision_###"`
- `confidence = "NOT_A_NUMBER"`

## 📊 Métriques et Rapports

### Score de Résilience

Le score est calculé selon :

```
Score = (Scénarios réussis + Récupérations réussies) / Total des tests * 100
```

### Rapport JSON

Chaque test génère un rapport dans `logs/chaos_reports/` :

```json
{
  "start_time": "2025-06-27T18:30:00",
  "test_duration": 60,
  "chaos_scenarios": [
    {
      "name": "config_corruption",
      "success": true,
      "duration": 12.34,
      "corrupted_files": [...]
    }
  ],
  "recovery_tests": [
    {
      "timestamp": "2025-06-27T18:31:00",
      "tests": [
        {
          "module": "modules.zeroia.core",
          "importable": true
        }
      ],
      "success": true
    }
  ],
  "overall_success": true,
  "actual_duration": 65.78
}
```

## 🛡️ Sécurité et Backups

### Système de Backup Automatique

- **Backup avant corruption** : Chaque fichier est sauvegardé
- **Répertoire** : `chaos_backups/`
- **Format** : `{filename}_{timestamp}.backup`
- **Restauration automatique** : En fin de test

### Mode Dry-Run

```bash
python scripts/chaos_test.py --dry-run
```

- **Simulation complète** : Aucune modification réelle
- **Logs identiques** : Même sortie que mode réel
- **Tests de récupération** : Simulation d'imports
- **Recommandé** : Pour développement

## 🔍 Exemple d'Exécution

```
🧪 [CHAOS] Démarrage test résilience (60s)...

🎯 [CHAOS] Scénario: config_corruption
💥 [CHAOS] Corruption fichiers configuration...
📦 [CHAOS] Backup: config/settings.toml → chaos_backups/settings_20250627_183000.toml.backup
💀 [CHAOS] Corrompu: config/settings.toml

🔍 [RECOVERY] Module modules.zeroia.core: ✅
🔍 [RECOVERY] Module modules.reflexia.core: ✅

📊 [CHAOS] RAPPORT DE TEST:
   ⏱️ Durée: 65.78s
   🎯 Scénarios: 5
   🔄 Tests récupération: 5
   ✅ Succès global: OUI
   📄 Rapport: logs/chaos_reports/chaos_test_report_20250627_183000.json

📈 [CHAOS] STATISTIQUES:
   💥 Scénarios réussis: 5/5
   🔄 Récupérations réussies: 5/5
   🛡️ Score de résilience: 100.0%
```

## 🚀 Intégration CI/CD

### GitHub Actions

```yaml
- name: 🧪 Chaos Testing
  run: |
    python scripts/chaos_test.py --dry-run --duration 30
```

### Tests automatiques

```bash
# Intégration dans tests
pytest tests/chaos/chaos_test.py -v
```

## ⚠️ Bonnes Pratiques

1. **Toujours tester en dry-run** avant production
2. **Backup manuel** des données critiques
3. **Tests programmés** en maintenance
4. **Monitoring actif** pendant les tests
5. **Documentation des résultats** pour amélioration continue

## 🔧 Dépannage

### Échec de Restauration

```bash
# Restauration manuelle
cp chaos_backups/*.backup /path/to/original/
```

### Logs de Debug

```bash
# Logs détaillés
python scripts/chaos_test.py --scenario config -v
```

### Reset Complet

```bash
# Nettoyage complet
rm -rf chaos_backups/
git checkout -- config/ modules/
```
