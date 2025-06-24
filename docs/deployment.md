# 🚀 Déploiement — Arkalia-LUNA

> Déployer Arkalia-LUNA proprement, avec Docker et GitHub, sur un serveur Linux local ou distant.

---

## 📦 Prérequis Déploiement

| Composant          | Détail                                 |
|--------------------|----------------------------------------|
| 🐧 **Serveur Linux**      | Ubuntu 20.04+ ou équivalent requis       |
| 🐋 **Docker + Compose**   | Conteneurisation des services IA         |
| 🔑 **Accès SSH**          | Pour les déploiements distants           |
| 🌐 **Ports ouverts**      | 8000 (API), 8001+ (modules IA si exposés) |

---

## ⚙️ Étapes de Déploiement

### 1. 🔧 Préparer le Serveur

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose git -y
sudo systemctl enable docker
```

### 2. 📂 Cloner le Dépôt

```bash
git clone https://github.com/arkalia-luna-system/arkalia-luna-pro.git
cd arkalia-luna-pro
```

### 3. 🔑 Configurer .env

Crée un fichier .env à la racine avec :

```
ARKALIA_ENV=prod
OLLAMA_HOST=http://localhost:11434
ARKALIA_SECRET_KEY=generate-a-key-here
```

Tu peux aussi y placer la config FastAPI, Docker ou logs.

⸻

### 4. 🚀 Lancer le Déploiement

```bash
docker-compose up -d --build
```

Vérifie ensuite l’accès sur :
➡️ http://<IP-serveur>:8000/

⸻

## 🤖 Meilleures Pratiques

| Aspect       | Recommandation                                      |
|--------------|-----------------------------------------------------|
| ⚙️ Automatisation | Utilise ark-clean-push, ark-docker-rebuild.sh     |
| 📊 Monitoring     | Installe htop, docker stats, ou prometheus       |
| 🔄 CI/CD          | GitHub Actions peut automatiser le déploiement   |
| 🔒 Sécurité       | Ne jamais exposer les clés .env en public        |


✅ **Vérification Post-Déploiement**
- Conteneurs actifs (`docker ps`)
- FastAPI accessible
- Logs OK (`logs/`, `htmlcov/`)
- Modules IA opérationnels

⸻

💡 Le déploiement d’Arkalia-LUNA est conçu pour être automatisable, stable et extensible, même sur une machine locale.
