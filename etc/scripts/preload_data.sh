#!/usr/bin/env bash
echo "Attempting to cron"
python3 /api/manage.py shell < /salic_ml_web/preload_data.py
