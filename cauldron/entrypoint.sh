#!/bin/bash

# Copy the settings_secret
cp /code/settings_secret.py /code/cauldron/Cauldron2/Cauldron2/settings_secret.py

# Run cauldron server
cd /code/cauldron/Cauldron2
echo "Apply migrations"
python3 manage.py makemigrations
python3 manage.py migrate
cd /code/cauldron/Cauldron2/MordredManager
echo "Run mordred manager that wait for new repositories for being analyzed"
python3 manager.py &
cd ..
echo "Start the cauldron server"
python3 manage.py runserver 0.0.0.0:8000
