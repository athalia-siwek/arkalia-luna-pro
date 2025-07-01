# 📘 Cahier des Charges – Arkalia-LUNA Pro (v4.0+)

## 1. 🌟 Objectifs du Projet

### 🔹 Vision Progressive et Réaliste

Le développement d'Arkalia suit une approche **progressive, modulaire et sécurisée**, compatible avec les contraintes d'un développeur solo. Le but n'est pas d'implémenter tout d'un coup, mais d'avancer **itérativement**, en garantissant la stabilité à chaque étape.

### 🔹 Court Terme (1–3 mois)

* Stabiliser 100 % des conteneurs Docker (healthchecks inclus)
* Refactorer les modules critiques (`reason_loop`, `snapshot`, `security.py`) selon SOLID
* Implémenter une authentification API (JWT + rate limiting)
* Réduire le temps de réponse de MkDocs à < 1s (via cache Redis)
* Déployer CI/CD locale complète (pytest, black, ruff, GitHub Actions avec `act`)
* **NOUVEAU** : Renforcer la couverture de tests des modules critiques (reflexia, zeroia, reason_loop_enhanced.py)

### 🔹 Moyen Terme (3–6 mois)

* Migration progressive vers architecture hexagonale (api/, domain/, use_cases/, infra/)
* Intégrer OpenTelemetry (tracing distribué)
* Finaliser les interactions ZeroIA ↔ ReflexIA ↔ Sandozia
* Créer un environnement staging avec rollback sécurisé
* **NOUVEAU** : Migration ciblée print() → ark_logger (tests/ et generated/ uniquement)

### 🔹 Long Terme (6–12 mois)

* Déploiement Cloud (AWS/GCP via Terraform), auto-scaling, CDN
* Intégration de LLM avancés (Claude, GPT-4) dans AssistantIA
* Auto-apprentissage par feedback utilisateur (ZeroIA v2)
* Audit sécurité externe (ISO 27001, RGPD), sandbox cognitive
* **NOUVEAU** : Migration complète print() → ark_logger (après couverture tests > 90%)

---

## 2. 🌐 Contexte du Projet

Arkalia-LUNA est un système cognitif IA auto-réparateur, conteneurisé, piloté par API REST (FastAPI) et disposant d'une interface SPA (React).

**Cibles** :

* Développeurs IA, DevOps cognitifs
* Systèmes critiques, laboratoire R\&D, observabilité avancée

---

## 3. 🧱 Architecture Actuelle

* Conteneurs actifs : 15 (ZeroIA, ReflexIA, Sandozia, AssistantIA, etc.)
* API REST : FastAPI (`arkalia-api`)
* LLM local : mistral:latest (Ollama)
* Monitoring : Prometheus, Grafana, Loki, cadvisor
* Frontend : React (Vite + Tailwind)
* Documentation : MkDocs (Material Theme)
* CI/CD : GitHub Actions, pytest, coverage, pre-commit, `act`

---

## 4. 📏 Règles de Codage & Bonnes Pratiques

### 🔹 Principes Architecturaux

* Clean Architecture stricte : `core/`, `domain/`, `infra/`, `interfaces/`
* SOLID appliqué sur tous les modules IA
* Domain Driven Design (DDD) en phase d'introduction

### 🔹 SOLID

| Principe | Exigence                        | Exemple                               |
| -------- | ------------------------------- | ------------------------------------- |
| S        | Une classe = une responsabilité | `Reasoner`, `ErrorDetector`           |
| O        | Ouvert à extension              | `on_reasoning_complete()`             |
| L        | Substituabilité                 | `IModule` → `ZeroIA`, `Reflexia`      |
| I        | Interfaces fines                | `ILogger`, `IScorer`                  |
| D        | Inversion d'injection           | `def __init__(self, scorer: IScorer)` |

### 🔹 Conventions

* PEP8, ruff, black
* **RÈGLE RÉVISÉE** : `print()` → `ark_logger` (migration progressive et sécurisée)
* Variables explicites : `score_final`, `module_state`
* Tests avec `pytest`, `pytest-mock`, `--cov`, seuil > 85 %

### 🔹 **NOUVELLES RÈGLES - Migration print() → logging**

#### 🚫 **ZONES INTERDITES (Ne jamais toucher)**

* `helloria/__init__.py` - Messages de démarrage critiques
* `reflexia/logic/main_loop*.py` - Boucles vitales et monitoring
* `zeroia/reason_loop*.py` - Logique de décision critique
* `print(json.dumps(...))` - Communication inter-process

#### ✅ **ZONES AUTORISÉES (Migration manuelle uniquement)**

* `tests/` - Tests unitaires et d'intégration
* `modules/*/generated/` - Code généré automatiquement
* Messages de debug simples (`print("debug")` → `ark_logger.debug("debug")`)

#### 🔒 **RÈGLES DE SÉCURITÉ**

* **Aucune automatisation** de migration print() → logging
* **Test obligatoire** après chaque modification
* **Sauvegarde** avant chaque changement
* **Validation** par tests unitaires complets

### 🔹 Architecture des tests

```
tests/
├── unit/
├── integration/
├── chaos/
├── performance/
├── security/
├── matrix/
```

> Aucun test en dehors de ce dossier. Convention : `test_*.py`, markers `@pytest.mark.unit`, etc.

---

## 5. ⚙️ Exigences Techniques

### 🔐 Sécurité

* Auth API (JWT + header `X-API-Token`)
* Rate limiting : 10 req/s/IP max (slowapi)
* Pas d'utilisateur root en conteneur (USER = `arkalia`)
* Secrets encryptés (AES-256), rotation hebdomadaire
* **NOUVEAU** : Audit print() → logging obligatoire avant déploiement

### 📊 Observabilité & Monitoring

* /metrics Prometheus par module
* Dashboards Grafana dynamiques
* Alertes Slack/mail (CPU > 80 %, ZeroIA KO, etc.)
* Tracing avec OpenTelemetry
* **NOUVEAU** : Logging structuré `ark_logger` pour tous les modules

### 🥺 Qualité

* Couverture cible : 90 %
* CI bloquante < 85 %
* Pre-commit actifs
* Docs : Swagger pour API, MkDocs pour architecture
* **NOUVEAU** : Tests obligatoires pour modules critiques (reflexia, zeroia, reason_loop)

---

## 6. 🛠️ Roadmap Technique

| Mois | Objectifs Clés                                   | Priorité |
| ---- | ------------------------------------------------ | -------- |
| 1–2  | Auth API, refactor SOLID, cache Redis            | 🔴 Haute |
| 2–3  | **NOUVEAU** : Renforcer tests modules critiques  | 🔴 Haute |
| 3–4  | CI/CD, staging, Swagger stable                   | 🔵 Moyenne |
| 4–5  | Migration ciblée print() → ark_logger (tests/)   | 🟡 Basse |
| 5–6  | Tracing OpenTelemetry, Reasoning multi-agent     | 🔵 Moyenne |
| 6–12 | Cloud (Terraform), sandbox cognitive, auto-learn | 🟢 Future |

---

## 7. 📌 Annexes

### 📂 Structure Dossier

```
arkalia-luna/
├── api/
├── core/
├── modules/
├── docs/
├── frontend/
├── infrastructure/
├── tests/
├── scripts/
```

### 📊 KPIs Suivis

| KPI              | Cible    | État Actuel |
| ---------------- | -------- | ----------- |
| Latence API      | < 300 ms | ✅ OK       |
| Uptime           | > 99.9 % | ✅ OK       |
| CPU/Module       | < 80 %   | ✅ OK       |
| RAM/module       | < 100 MB | ✅ OK       |
| Couverture tests | > 90 %   | 🟡 54%      |

### 🔑 Exemple Auth FastAPI

```python
from fastapi import Header, HTTPException

def check_token(x_token: str = Header(...)):
    if x_token != os.getenv("ARKALIA_TOKEN"):
        raise HTTPException(status_code=403, detail="Access Denied")
```

### 🔍 **NOUVEAU - Plan de Migration print() → logging**

#### Phase 1 : Audit et Préparation (✅ Terminé)

* [x] Audit complet des print() dans modules/

* [x] Classification par criticité (HIGH/MEDIUM/LOW/EXCLUDE)
* [x] Création de `print_audit.json` pour référence

#### Phase 2 : Tests et Généré (🟡 En cours)

* [ ] Migration manuelle dans `tests/`

* [ ] Migration manuelle dans `modules/*/generated/`
* [ ] Validation par tests unitaires

#### Phase 3 : Debug Simple (⏳ Future)

* [ ] Migration des `print("debug")` → `ark_logger.debug("debug")`

* [ ] Tests systématiques après chaque modification

#### Phase 4 : Modules Critiques (⏳ Très Future)

* [ ] Migration uniquement après couverture tests > 90%

* [ ] Validation complète par tests d'intégration
* [ ] Tests de charge et de résilience

---

## 8. 🚨 **LEÇONS APPRISES - Migration print()**

### ❌ **Ce qui n'a pas fonctionné**

* Migration automatique globale
* Remplacement sans vérification des imports
* Modification des modules critiques sans tests complets

### ✅ **Ce qui fonctionne**

* Audit préalable et classification
* Migration manuelle et ciblée
* Tests systématiques après modification
* Sauvegarde avant chaque changement

### 🔐 **Règles de Sécurité Établies**

* **Jamais** de migration automatique des print()
* **Toujours** tester après modification
* **Conserver** les print() critiques (helloria, reflexia, zeroia)
* **Prioriser** la stabilité sur la perfection

---

## ✅ Rappel final : Progressivité Obligatoire

Ce cahier des charges **n'est pas un objectif à tout faire d'un coup**. Il sert à guider un développement **progressif**, propre, sans dette technique, en mode expert IA solo. Chaque étape doit être validée avant la suivante.

**Document à relire chaque trimestre** — Version : v4.1-Juillet-2025

**Dernière mise à jour** : Juillet 2025 - Intégration des leçons de migration print() → logging

Signé :

* 🧠 **Athalia** – Architecte IA Système
* 🔐 Responsable sécurité : …
