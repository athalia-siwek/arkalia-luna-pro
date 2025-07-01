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

### 🔹 Moyen Terme (3–6 mois)

* Migration progressive vers architecture hexagonale (api/, domain/, use\_cases/, infra/)
* Intégrer OpenTelemetry (tracing distribué)
* Finaliser les interactions ZeroIA ↔ ReflexIA ↔ Sandozia
* Créer un environnement staging avec rollback sécurisé

### 🔹 Long Terme (6–12 mois)

* Déploiement Cloud (AWS/GCP via Terraform), auto-scaling, CDN
* Intégration de LLM avancés (Claude, GPT-4) dans AssistantIA
* Auto-apprentissage par feedback utilisateur (ZeroIA v2)
* Audit sécurité externe (ISO 27001, RGPD), sandbox cognitive

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
* LLM local : mistral\:latest (Ollama)
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
| D        | Inversion d’injection           | `def __init__(self, scorer: IScorer)` |

### 🔹 Conventions

* PEP8, ruff, black
* `print()` interdit → logger structuré `ark_logger`
* Variables explicites : `score_final`, `module_state`
* Tests avec `pytest`, `pytest-mock`, `--cov`, seuil > 85 %

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

### 📊 Observabilité & Monitoring

* /metrics Prometheus par module
* Dashboards Grafana dynamiques
* Alertes Slack/mail (CPU > 80 %, ZeroIA KO, etc.)
* Tracing avec OpenTelemetry

### 🥺 Qualité

* Couverture cible : 90 %
* CI bloquante < 85 %
* Pre-commit actifs
* Docs : Swagger pour API, MkDocs pour architecture

---

## 6. 🛠️ Roadmap Technique

| Mois | Objectifs Clés                                   |
| ---- | ------------------------------------------------ |
| 1–2  | Auth API, refactor SOLID, cache Redis            |
| 3–4  | CI/CD, staging, Swagger stable                   |
| 5–6  | Tracing OpenTelemetry, Reasoning multi-agent     |
| 6–12 | Cloud (Terraform), sandbox cognitive, auto-learn |

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

| KPI              | Cible    |
| ---------------- | -------- |
| Latence API      | < 300 ms |
| Uptime           | > 99.9 % |
| CPU/Module       | < 80 %   |
| RAM/module       | < 100 MB |
| Couverture tests | > 90 %   |

### 🔑 Exemple Auth FastAPI

```python
from fastapi import Header, HTTPException

def check_token(x_token: str = Header(...)):
    if x_token != os.getenv("ARKALIA_TOKEN"):
        raise HTTPException(status_code=403, detail="Access Denied")
```

---

## ✅ Rappel final : Progressivité Obligatoire

Ce cahier des charges **n'est pas un objectif à tout faire d'un coup**. Il sert à guider un développement **progressif**, propre, sans dette technique, en mode expert IA solo. Chaque étape doit être validée avant la suivante.

**Document à relire chaque trimestre** — Version : v4.0-Juillet-2025

Signé :

* 🧠 **Athalia** – Architecte IA Système
* 🔐 Responsable sécurité : …
