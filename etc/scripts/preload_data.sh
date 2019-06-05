#!/usr/bin/env bash
echo "======================= $(date) ======================="
echo "Recalculating metrics"
cd /
cat /etc/env/django.env /etc/env/postgres.env > /cronvars.env
. /cronvars.env /usr/local/bin/inv get-pickles
. /cronvars.env /usr/local/bin/inv update-models train-metrics
rm /cronvars.env
