#!/bin/bash

# Run cauldron server
cd /code/cauldron/Cauldron2
echo "Apply migrations"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Start the cauldron server"
python3 manage.py runserver 0.0.0.0:8000
