# 🧩 Modules actifs
🔁 reflexia/ — Réflexion adaptative & surveillance système

Supervise l’état global du système, détecte les dérives, applique des correcteurs. C’est l’observateur réflexif central du noyau Arkalia.

⸻

📱 nyxalia/ — Interface & interactions mobiles

Sert de pont entre Arkalia et les couches d’interface (mobile, vocale, API externes). Focalisé sur la communication fluide et naturelle.

⸻

🌐 helloria/ — Lien FastAPI & serveurs locaux

Démarre et orchestre l’API locale FastAPI. Sert de passerelle entre les modules internes et les interfaces REST.


Chaque module suit la structure :
modules/<nom_module>/
├── init.py
├── core.py
├── config/
├── state/
├── logs/
├── tests/
├── utils/

Chaque module est isolé, testable, extensible.