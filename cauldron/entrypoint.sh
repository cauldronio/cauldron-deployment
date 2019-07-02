#!/bin/bash

echo "Apply migrations"
python3 /code/cauldron/Cauldron2/manage.py makemigrations
python3 /code/cauldron/Cauldron2/manage.py migrate

echo "Start the cauldron server"
cd /code/cauldron/Cauldron2/
python3 manage.py runserver 0.0.0.0:8000