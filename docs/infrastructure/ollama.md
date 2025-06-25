# 🧠 Ollama — Modèles LLM Locaux

> Intégration de modèles LLM **100 % locaux**, sans cloud, via l’outil **[Ollama](https://ollama.com/)**.

---

## 📁 Chemin de Stockage

Les modèles sont stockés ici :

```bash
/Volumes/T7/devstation/ollama_data/models
```

## 📦 Modèles Installés

| Nom       | Taille approx. | Utilisation principale                      |
|-----------|----------------|---------------------------------------------|
| mistral   | ~4.1 Go        | Génération IA contextuelle rapide           |
| llama2    | ~3.8 Go        | Modèle polyvalent, bon en généraliste       |
| tinyllama | ~637 Mo        | LLM ultra-léger pour tests rapides          |

💡 D’autres modèles peuvent être installés à la volée avec :

```bash
ollama pull <nom_du_modèle>
```

## ⚙️ Configuration de l’Environnement

Ajoutez dans votre fichier `~/.zshrc` :

```bash
export OLLAMA_MODELS=/Volumes/T7/devstation/ollama_data/models
```

Ensuite, rechargez le shell :

```bash
source ~/.zshrc
```

## 🔧 Exemple d’appel via API (Ollama Serveur Local)

```bash
curl http://localhost:11434/api/generate \
  -d '{
        "model": "mistral",
        "prompt": "Bonjour, peux-tu m’aider à automatiser une tâche ?"
      }'
```

## 🔐 Intégration dans Arkalia

- Le connecteur `ollama_connector.py` est disponible dans `utils/`
- Le module AssistantIA utilise `query_ollama()` pour générer des réponses locales.
- Les logs sont capturés dans `logs/assistantia/`.

⸻

🧠 Arkalia-LUNA exécute ses IA localement, pour préserver la confidentialité et maximiser l’efficacité cognitive.
