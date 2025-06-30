# Sandozia — Intelligence croisée

Sandozia est le module d'intelligence croisée du kernel Arkalia-LUNA. Il fonctionne en mode daemon (pas d'API HTTP publique) et prend en charge :

- L'analyse avancée des états et décisions
- La validation de la cohérence inter-modules (ZeroIA, ReflexIA)
- Le support à la prise de décision

**Entrée/Sortie :**
- Dialogue via fichiers d'état et events
- Expose ses métriques via arkalia-api (pas directement)

**Cas d'usage :**
- Analyse croisée
- Détection de divergences
- Support décisionnel

**Pas d'API HTTP publique** : toute interaction passe par arkalia-api ou les fichiers d'état internes.
