#!/usr/bin/env bash


cd src/api/
python3 manage.py makemigrations
python3 manage.py migrate

echo "** Attempting to start service **"
python3 manage.py runserver 0.0.0.0:8080