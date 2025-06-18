# 🛡️ SECURITY.md — Politique de sécurité Arkalia-LUNA

Merci de contribuer à la sécurité d'Arkalia-LUNA.

## 📬 Signalement de vulnérabilités

Si vous découvrez une faille, **merci de ne pas l’annoncer publiquement**. Contactez-nous directement via :

- 📧 Email : athalia.security@arkalia.system (ou méthode sécurisée à définir)
- 🔐 Clé PGP : (à ajouter)

## ✅ Bonnes pratiques recommandées

- Ne jamais exposer les fichiers `state/`, tokens ou secrets dans des commits publics.
- Utiliser un `.env` local et l’ajouter au `.gitignore`.
- Analyser les dépendances régulièrement (`pip list --outdated` ou `pip-audit`).

## 📦 Outils recommandés

- `bandit` : scan de vulnérabilités Python
- `pip-audit` : vérification des dépendances

---

*Dernière mise à jour : 2025-06-18*
