# 📚 Documentation Arkalia-LUNA

Bienvenue dans la documentation officielle d’**Arkalia-LUNA** — un système cognitif IA **local**, **modulaire**, **auto-réflexif** et **entièrement versionné**.

Cette base documente l’ensemble des composants d’Arkalia : modules actifs, API locale, scripts intelligents, logique de tests, automatisation et intégration de modèles IA locaux (LLMs).

---

## 🧠 Modules IA actifs

| Module     | Rôle principal                                    |
|------------|---------------------------------------------------|
| `reflexia` | Réflexion adaptative, pondération, auto-surveillance |
| `zeroia`   | Raisonnement logique, décisions contextuelles     |
| `nyxalia`  | Interfaces mobiles et externes                    |
| `helloria` | Passerelle FastAPI et serveur local               |

---

## ⚙️ Fonctionnalités couvertes

- 🧠 Modules IA actifs et orchestrables
- ⚙️ API FastAPI (`/status`, `/module/trigger`, etc.)
- 🧬 Architecture du noyau (`core`, `modules`, `state`, `logs`, etc.)
- 🔁 Scripts d’orchestration (`ark-test`, `ark-docker`, `trigger_scan.sh`)
- 🧪 Tests & CI : `pytest`, `ruff`, `black`, `GitHub Actions`
- 🐳 Docker : `docker-compose`, build sans cache, image locale propre

---

## 🧠 Intégration LLM locale (via Ollama)

> Arkalia utilise des **modèles IA locaux** via [**Ollama**](https://ollama.com), stockés en externe pour préserver l’environnement principal.

**Modèles disponibles :**
- `mistral` (7B)
- `tinyllama` (1.1B)
- `llama2` (7B, 13B)

📁 **Chemin de stockage externe :**  
`/Volumes/T7/devstation/ollama_data/models/`

➡ Plus d'infos : [`arkalia-ollama`](https://github.com/arkalia-luna-system/arkalia-ollama)

---

## 🔄 Synchronisation & documentation automatique

> Chaque mise à jour du code entraîne une synchronisation automatique de la documentation via **MkDocs + GitHub Actions**.

📘 Documentation publique :  
[`arkalia-luna-system.github.io/arkalia-luna-pro`](https://arkalia-luna-system.github.io/arkalia-luna-pro)

---

![🧠 Diagramme de l’architecture Arkalia](img/diagram_kernel.png)

🧭 *Arkalia-LUNA est un système IA évolutif, conçu pour durer, s’adapter, et orchestrer intelligemment ses modules internes.*

---

Maintenu par **Athalia 🌙** — [`github.com/arkalia-luna-system`](https://github.com/arkalia-luna-system)