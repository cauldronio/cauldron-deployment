#!/bin/bash

# Copy the settings_secret
cp /code/settings_secret.py /code/cauldron/Cauldron2/Cauldron2/settings_secret.py

# Create a database for mordred
until mysql -u grimoirelab -h grimoirelab_service -e "CREATE DATABASE IF NOT EXISTS test_sh;"
do
  echo $(date +"%x %X") - Waiting for mysql
  sleep 2
done

# Run cauldron server
cd /code/cauldron/Cauldron2
echo "Apply migrations"
python3 manage.py makemigrations
python3 manage.py migrate
cd /code/cauldron/Cauldron2/MordredManager
echo "Run mordred manager that waits for new repositories for being analyzed"
python3 manager.py &
cd ..
echo "Start the cauldron server"
python3 manage.py runserver 0.0.0.0:8000
