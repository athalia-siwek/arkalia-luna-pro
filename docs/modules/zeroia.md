# ZeroIA — Décisionneur autonome

ZeroIA est le module de décision autonome du kernel Arkalia-LUNA. Il fonctionne en mode daemon (pas d'API HTTP publique) et prend en charge :

- La prise de décision automatique (monitoring, réduction de charge, emergency shutdown)
- Le circuit breaker (protection contre les boucles d'échec)
- L'auto-récupération (error recovery)
- L'intégrité du contexte et la cohérence des décisions

**Entrée/Sortie :**

- Interagit avec Reflexia et Sandozia via fichiers d'état et events
- Expose ses métriques via arkalia-api (port 8000) (pas directement)

**Cas d'usage :**

- Surveillance continue
- Protection adaptative
- Décision rapide en cas d'anomalie

**Pas d'API HTTP publique** : toute interaction passe par arkalia-api (port 8000) ou les fichiers d'état internes.
