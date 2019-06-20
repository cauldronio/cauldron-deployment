#!/bin/bash

echo "Apply migrations"
python3 /code/cauldron/Cauldron2/manage.py makemigrations
python3 /code/cauldron/Cauldron2/manage.py migrate

rm /etc/nginx/sites-enabled/default
supervisord
supervisorctl reread
supervisorctl update
supervisorctl restart cauldron

if [[ $CERTBOT_ENABLED -eq 1 ]]; then
    certbot --nginx -n -d $CERTBOT_DOMAIN --agree-tos --email $CERTBOT_MAIL
fi
service nginx restart


tail -f /dev/null