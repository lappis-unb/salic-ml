#!/usr/bin/env bash
echo "Attempting to cron"
inv get-pickles
inv update-models train-metrics

