#!/bin/bash

# Specify your test run number here
RUN_NUMBER=17

rm -rf workspaces/*

# bash DANGER_purge_openhands_containers.sh

LOG_FILE="test_run_${RUN_NUMBER}_ghcr.log"

echo "Starting test run $RUN_NUMBER..."
echo "Logging output to $LOG_FILE"

# Execute the python script and redirect stdout and stderr to the log file
python main.py &> "$LOG_FILE"

# bash get_docker_logs.sh