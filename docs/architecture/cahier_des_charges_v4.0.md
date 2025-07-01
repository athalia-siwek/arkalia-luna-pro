# 📘 Cahier des Charges – Arkalia-LUNA Pro (v4.0+)

## 1. 🎯 Objectifs du Projet

### 🔹 Court Terme (1–3 mois)

- Stabiliser 100 % des conteneurs (Docker, healthchecks actifs).
- Refactoriser les modules critiques (reason_loop, snapshot, security.py) selon SOLID.
- Implémenter une authentification API (JWT + rate limiting).
- Réduire le temps de réponse de MkDocs à < 1s (via cache Redis).
- Déployer la CI/CD complète avec pytest, black, ruff, act, GitHub Actions.

### 🔹 Moyen Terme (3–6 mois)

- Migrer l'architecture vers microservices hexagonaux avec interfaces claires (api/, use_cases/, infra/).
- Intégrer OpenTelemetry pour le tracing distribué.
- Finaliser le raisonnement multi-agent ZeroIA ↔ ReflexIA ↔ Sandozia.
- Créer un environnement staging complet avec rollback sécurisé.

### 🔹 Long Terme (6–12 mois)

- Déploiement Cloud (AWS/GCP) avec Terraform, auto-scaling, reverse proxy, CDN.
- Intégration de LLM avancés (Claude, GPT-4) dans AssistantIA.
- Auto-apprentissage par feedback utilisateur (ZeroIA v2).
- Audit externe sécurité (ISO 27001, RGPD), sandbox cognitive.

---

## 2. 🌐 Contexte du Projet

Arkalia-LUNA est un système IA modulaire, auto-réparateur, auto-observant, fonctionnant via une architecture Dockerisée, piloté par une API REST centrale (FastAPI), et doté d'une interface web moderne (React).

**Public :**

- Développeurs IA / Ops cognitifs
- Systèmes critiques et haute résilience
- R&D, laboratoires, entreprises tech innovantes

---

## 3. 🧱 Architecture Actuelle

- Microservices Dockerisés : 15 conteneurs actifs (ZeroIA, ReflexIA, AssistantIA…)
- LLM Local : mistral:latest via Ollama
- Monitoring : Grafana, Prometheus, Loki, cadvisor, node-exporter
- Frontend : React (Vite + Tailwind), SPA
- Backend : FastAPI + docs Swagger
- Documentation : MkDocs (Material Theme)
- CI/CD : GitHub Actions (act), pytest, coverage, pre-commit

```
C4Context
    title "Arkalia-LUNA – Architecture Globale"
    Enterprise_Boundary(b0, "Infra") {
        System(arkalia_api, "arkalia-api", "FastAPI REST")
        System(user, "Utilisateur", "Dashboard React / API")
        System_Ext(llm, "Ollama", "mistral:latest")
    }
    Rel(user, arkalia_api, "Utilise")
    Rel(arkalia_api, llm, "Interroge")
```

---

## 4. 📏 Règles de Codage & Bonnes Pratiques

### 🔹 Architecture & Structure

- Clean Architecture stricte : core/, domain/, interfaces/, use_cases/, infra/
- 1 fonction = 1 responsabilité (Single Responsibility)
- Séparation stricte logique métier ↔ adaptateurs

### 🔹 Principes SOLID appliqués

| Principe | Exigence | Exemple |
|----------|----------|---------|
| S | Une classe = une seule responsabilité | Reasoner, ErrorDetector |
| O | Ouvert à extension | Hook on_reasoning_complete() |
| L | Modules IA substituables | class IModule → ZeroIA, Reflexia |
| I | Interfaces fines | ILogger, IScorer séparés |
| D | Abstractions > implémentations | def **init**(self, scorer: IScorer) |

### 🔹 Conventions Python & Outils

- PEP8 strict (black, ruff avec règles sévères)
- Variables claires : reason_score, module_state
- print() interdit → logger structuré ark_logger
- Tests avec pytest, pytest-mock, --cov + seuil : 85 %

### 🔹 Architecture des Tests

- **Structure stricte** : tous les tests dans `tests/` uniquement
  - `tests/unit/` : tests unitaires par module
  - `tests/integration/` : tests d'intégration par service
  - `tests/chaos/` : tests de résilience et chaos engineering
  - `tests/performance/` : tests de performance
  - `tests/security/` : tests de sécurité
  - `tests/matrix/` : tests combinatoires et edge cases

- **Interdiction** : aucun test dans `modules/`, `scripts/`, `routes/`
- **Imports relatifs** : utilisation de `sys.path.insert()` pour les imports absolus
- **Convention de nommage** : `test_*.py` pour tous les fichiers de test
- **Markers pytest** : `@pytest.mark.unit`, `@pytest.mark.integration`, etc.

### 🔹 Gestion des Imports

- **Ordre des imports** : stdlib → third-party → local (PEP8)
- **Imports absolus** : préférés pour les modules du projet
- **Imports relatifs** : uniquement pour les sous-modules du même package
- **Path dynamique** : `sys.path.insert()` pour les tests avec imports complexes
- **Éviter** : imports circulaires et imports conditionnels

---

## 5. ⚙️ Exigences Techniques

### 🔐 Sécurité

- Authentification JWT + token header (X-API-Token)
- Rate limiting dynamique (slowapi) : max 10 req/s/IP
- Aucune élévation root dans Docker (USER arkalia)
- Secrets encryptés (AES-256, rotation hebdo)

### 📊 Monitoring & Observabilité

- Prometheus + /metrics par module
- Grafana : dashboards par module, heatmap cognitive
- Alertmanager + alertes Slack/mail : CPU > 80 %, ZeroIA KO
- Tracing distribué avec OpenTelemetry

### 🧪 Qualité logicielle

- Couverture minimale 90 %
- CI bloquante si < 85 % (via GitHub Actions + act)
- Tests containers (Docker) avec pytest-docker
- Documentation Swagger + MkDocs (versionnée)
- Convention Git (vX.Y.Z, changelogs, PRs nettes)

---

## 6. 🛠️ Roadmap Technique (12 mois)

| Période | Objectifs principaux | Modules/Actions |
|---------|---------------------|-----------------|
| Mois 1–2 | Auth API, refactor SOLID, cache Redis | api, core, docs |
| Mois 2–4 | CI/CD complète, exposition Swagger, staging | ci, infra, docker |
| Mois 4–6 | Tracing, multi-agent loop | reactor, zeroia, reflexia |
| Mois 6–12 | Cloud (Terraform), audit sécurité, IA avancée | assistantia, cloud |

---

## 7. 📎 Annexes

### 📌 Structure de Dossiers

```
arkalia-luna/
├── api/                  # FastAPI
├── core/                 # Logique métier
├── modules/              # IA : zeroia/, reflexia/, sandozia/
├── docs/                 # MkDocs
├── frontend/             # React
├── infrastructure/       # Docker, Terraform, Prometheus…
├── tests/                # Tests unitaires/integration
└── scripts/              # CI/CD, analyse statique
```

### 📌 KPIs Clés à Suivre

| KPI | Objectif |
|-----|----------|
| Latence API (P95) | < 300 ms |
| Couverture tests | > 90 % |
| Uptime mensuel | ≥ 99.9 % |
| CPU moyen / conteneur | < 80 % |
| RAM / module | < 100 MB |

### 📌 Exemple Auth FastAPI

```python
from fastapi import Header, HTTPException

def check_token(x_token: str = Header(...)):
    if x_token != os.getenv("ARKALIA_TOKEN"):
        raise HTTPException(status_code=403, detail="Access Denied")
```

---

## ✅ Résumé Final

Arkalia-LUNA Pro est désormais un système IA modulaire, sécurisé, versionné, et monitoré, prêt à passer à l'échelle. Ce cahier des charges assure la conformité pro, la stabilité cognitive et la maintenabilité.

**Document à réviser tous les trimestres. Version actuelle : v4.0-Juin-2025**

**Signatures :**

- 🧠 **Athalia** – Architecte IA Système
- 🔐 **Responsable Sécurité** : …
