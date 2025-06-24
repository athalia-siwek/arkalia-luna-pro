---

## ✅ `/docs/automation.md` — Version améliorée

```markdown
# 🧠 Scripts & Automatisation — Arkalia-LUNA

Arkalia n’est pas simplement automatisée : elle est **auto-orchestrée**.

Son cœur repose sur des **scripts Bash intelligents**, interfacés avec les modules IA pour une gestion proactive, auto-corrective et dynamique.

---

## 🔁 Boucle Maîtresse — `arkalia_master_loop.py`

La boucle principale du système :

- 🧩 Charge dynamiquement tous les modules déclarés (`config/`)
- 🔁 Réinjecte les derniers états sauvegardés (`state/`)
- 📊 Analyse les logs récents pour détecter les dérives
- 🤖 Laisse ReflexIA ou ZeroIA décider d’actions automatiques :
  - restart de module
  - forçage d’un `pytest`
  - déclenchement d’un `ark-clean-push`
  - interruption d’un service incohérent

---

## ⚙️ Scripts opérationnels

| Script                   | Fonction principale                                               |
|--------------------------|-------------------------------------------------------------------|
| `ark-bootstrap`          | Initialise l’environnement local (`venv`, pre-commit, etc.)       |
| `ark-test`               | Lance tous les tests `pytest` + rapport de couverture             |
| `ark-docs`               | Compile la documentation MkDocs en local                          |
| `ark-docker`             | Lance l’API via Docker (`docker-compose up`)                      |
| `ark-docker-rebuild.sh`  | Rebuild complet du container (`build`, `up`, `logs`)              |
| `trigger_scan.sh`        | Déclenche manuellement une analyse réflexive (Reflexia)           |
| `ark-clean-push`         | Format `black`, lint `ruff`, commit Git et push sécurisé          |

---

## 🧠 Orchestration cognitive

Modules intelligents comme `reflexia/` ou `zeroia/` peuvent automatiquement :

- suspendre des modules en surcharge
- redémarrer un service figé
- corriger un état incohérent dans `state/`
- vérifier les `logs/` et décider de relancer une boucle de test

---

💡 *Cette orchestration transforme Arkalia en un **système IA auto-régulé**, sans besoin d’intervention humaine constante.*
