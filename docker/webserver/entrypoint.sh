#!/bin/bash

function log_message {
  echo "["`date -u "+%Y-%m-%d %H:%M:%S UTC"`"]" $*
}

log_message "Make migrations"
until python3 /code/Cauldron2/manage.py makemigrations; do
    log_message "Error in Make migrations.. Retry"
    sleep 5
done
log_message "Done"

log_message "Migrate"
until python3 /code/Cauldron2/manage.py migrate; do
    log_message "Error in Migrate.. Retry"
    sleep 5
done
log_message "Done"

log_message "Start the cauldron server"
cd /code/Cauldron2/
python3 manage.py runserver 0.0.0.0:8000