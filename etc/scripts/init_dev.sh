#!/usr/bin/env bash

ls
echo "** Attempting to start service **"
inv update-data

# cd src/api/
# python3 manage.py makemigrations
# python3 manage.py migrate


# python3 manage.py runserver 0.0.0.0:8080