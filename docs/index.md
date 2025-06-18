# 📚 Documentation Arkalia-LUNA

Bienvenue dans la documentation technique d’**Arkalia-LUNA**, un système cognitif IA local, **modulaire**, **auto-réflexif** et **entièrement documenté**.

Cette documentation couvre l’ensemble des composants : modules actifs, API locale, scripts d’orchestration, tests, automatisation et intégration de modèles IA (LLM).

---

## 🧠 Modules actifs

- `reflexia` — Réflexion adaptative et surveillance système  
- `zeroia` — Raisonnement logique et décisions contextuelles  
- `nyxalia` — Interfaces mobiles et externes  
- `helloria` — Passerelle FastAPI et serveur local  

---

## ⚙️ Fonctionnalités couvertes dans la documentation

- 🧠 **Modules IA actifs**
- ⚙️ **API FastAPI** (avec endpoints `/status`, `/module/trigger`, etc.)
- 🧬 **Structure du noyau** (kernel & devstation)
- 🔁 **Scripts & automatisation** (`ark-test`, `ark-docker-rebuild.sh`, etc.)
- 🧪 **Tests unitaires & CI/CD** (pytest, ruff, GitHub Actions)
- 🐳 **Docker & déploiement local**

---

## 🔁 Configuration locale des modèles (Ollama)

> Utilisation des modèles LLM **localement avec `ollama`**, sans consommer l’espace disque interne du Mac.

➡ Voir le dépôt dédié : [arkalia-ollama (GitHub)](https://github.com/athalia-siwek/arkalia-ollama)

### ✅ Modèles installés :
- `mistral`
- `tinyllama`
- `llama2`

📁 **Chemin de stockage** :  
`/Volumes/T7/devstation/ollama_data/models`

---

🧭 *Cette documentation évolue en parallèle du système IA. Toute mise à jour majeure de code est automatiquement synchronisée avec cette page via GitHub Actions (MkDocs).*  