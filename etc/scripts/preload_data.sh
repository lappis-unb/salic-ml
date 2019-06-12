#!/bin/sh
echo "======================= $(date) ======================="
cd /
cat /etc/env/*.env | sed '/^$/d' > /cronvars.env
cat /cronvars.env | sed 's/^/export /' > /exportvars.env
. /exportvars.env
. /cronvars.env
echo "Recalculating metrics"
/usr/local/bin/inv get-pickles && /usr/local/bin/inv update-models train-metrics
echo "Done"
exit 0
