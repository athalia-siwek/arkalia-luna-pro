# 🧩 Composants d’Arkalia-LUNA

> Vue d’ensemble des composants actifs dans le système IA Arkalia-LUNA.

---

## 🧠 Composants principaux

| Composant     | Rôle |
|---------------|------|
| **Reflexia**  | Supervise la cognition et applique des pondérations adaptatives. |
| **ZeroIA**    | Réalise des raisonnements logiques et prend des décisions contextuelles. |
| **Nyxalia**   | Sert de passerelle mobile et vocale (interfaces externes). |
| **Helloria**  | Démarre l’API FastAPI, relie les modules internes et les interfaces REST. |
| **Sandozia** *(à venir)* | Module de cybersécurité cognitive et d’analyse comportementale. |
| **ArkaliaLoop** | Orchestre l’activation séquentielle des modules IA. |

---

## 🔁 Collaboration des composants

- `Reflexia` analyse les logs → propose des décisions.
- `ZeroIA` raisonne → déclenche ou suspend un module.
- `Nyxalia` capte une intention vocale → la transmet via `Helloria`.
- `Helloria` expose les endpoints vers l’extérieur ou vers `AssistantIA`.

Chaque composant peut être mis à jour indépendamment.

---

## ⚙️ Architecture modulaire

- Maintenance facilitée
- Évolutivité immédiate
- Séparation stricte des responsabilités

---

💡 *La modularité d’Arkalia-LUNA est pensée pour durer, évoluer et s’adapter à l’usage cognitif réel.*
