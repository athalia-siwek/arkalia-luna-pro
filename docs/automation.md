# 🤖 Scripts & Automatisation

Arkalia fonctionne principalement via **scripts bash** et **boucles orchestrées**.

## 🔄 Boucle master : `arkalia_master_loop.py`

Cette boucle charge dynamiquement :

- Les modules déclarés dans `config/`
- Les états persistants depuis `state/`
- Les logs pour audit intelligent
- Les décisions reflexIA automatiques

## ⚙️ Scripts importants

| Script                         | Rôle                                   |
|-------------------------------|----------------------------------------|
| `ark-bootstrap`               | Démarrage de l’environnement IA        |
| `ark-test`                    | Lancement des tests + couverture       |
| `ark-docker-rebuild.sh`       | Rebuild du container local             |
| `trigger_scan.sh`             | Lance reflexIA manuellement            |
| `ark-clean-push`              | Black + Ruff + Git push intelligent    |

---

💡 *Chaque action peut être pilotée par ZeroIA ou ReflexIA selon les priorités du système.*