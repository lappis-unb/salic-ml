#!/usr/bin/env bash

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
echo "** Attempting to start service **"
python3 manage.py runserver 0.0.0.0:8080
