#!/bin/bash

echo "🛡️  Test Fail2Ban Jail — arkalia-nginx"
echo "--------------------------------------"

# Vérifie que le fichier log nginx existe
if [ ! -f /var/log/nginx/access.log ]; then
  echo "⛔ Fichier /var/log/nginx/access.log introuvable. Êtes-vous dans le bon conteneur ?"
  exit 1
fi

# Injection de logs suspects
echo "[🔁] Injection de requêtes /admin dans /var/log/nginx/access.log"
for i in {1..10}; do
  echo '192.168.1.100 - - [26/Jun/2025:08:11:00] "GET /admin HTTP/1.1" 404 234' >> /var/log/nginx/access.log
done

# Reload de Fail2Ban
echo "[🔄] Reload de Fail2Ban..."
fail2ban-client reload

sleep 2

# Statut de la jail
echo "[📊] Statut de la jail arkalia-nginx :"
fail2ban-client status arkalia-nginx || echo "⚠️  Impossible de lire le statut de la jail."

# Logs fail2ban (si fichier dispo)
if [ -f /var/log/fail2ban.log ]; then
  echo "[📁] Dernières lignes du log fail2ban :"
  tail -n 5 /var/log/fail2ban.log
else
  echo "⚠️  Aucun fichier /var/log/fail2ban.log trouvé (log désactivé ou autre nom)."
fi

echo "✅ Test terminé."
