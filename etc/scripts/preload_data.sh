#!/usr/bin/env bash
echo "Attempting to cron"
inv update-data --pickles
inv update-models train-metrics

