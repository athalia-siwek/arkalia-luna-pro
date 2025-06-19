# 🛡️ SECURITY.md — Politique de sécurité Arkalia-LUNA

Merci de contribuer à la sécurité d'Arkalia-LUNA.

## 📬 Signalement de vulnérabilités

Si vous découvrez une vulnérabilité, **merci de ne pas la divulguer publiquement**.  
Veuillez nous contacter via l’un des moyens suivants :

- 📧 Email : [athalia.security@arkalia.system](mailto:athalia.security@arkalia.system)
- 🔐 Clé PGP publique : *(à publier prochainement)*

Nous nous engageons à répondre dans un délai de 72 heures.

---

## ✅ Bonnes pratiques recommandées

- **Ne jamais exposer** les fichiers sensibles (`state/`, tokens, clés API) dans un dépôt public.
- **Utiliser** un fichier `.env` pour les variables secrètes, et l’inclure dans le `.gitignore`.
- **Analyser régulièrement** les dépendances avec :
  - `pip list --outdated`
  - `pip-audit` ou `safety`

---

## 🔧 Outils de sécurité recommandés

| Outil        | Description                                      | Installation              |
|--------------|--------------------------------------------------|---------------------------|
| `bandit`     | Détecte les vulnérabilités dans le code Python   | `pip install bandit`     |
| `pip-audit`  | Scanne les packages pour failles connues         | `pip install pip-audit`  |
| `safety`     | Alternative à `pip-audit`                        | `pip install safety`     |

---

## 🔐 À venir

- 🔑 Publication de la clé PGP officielle
- ✅ Intégration de `pip-audit` dans la CI
- 🧪 Script `ark-secure-check.sh` pour audit automatique

---

*📅 Dernière mise à jour : 2025-06-19 — Maintenu par Athalia*