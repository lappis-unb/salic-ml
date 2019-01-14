#!/usr/bin/env bash
echo "Attempting to cron"
python3 /salic_ml_web/manage.py shell < /salic_ml_web/preload_data.py
