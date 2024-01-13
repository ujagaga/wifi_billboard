#!/bin/bash

# This script should be run as user, and the app will be available via port 80
SCRIPT_RELATIVE_PATH=$(dirname "$0")
SCRIPT_FULL_PATH="$(realpath -s $0)"
SCRIPT_DIR="$(dirname $SCRIPT_FULL_PATH)"

sudo apt update
sudo apt -y install -y v4l-utils python3-fastapi uvicorn

SERVICE_NAME=billboard.service
SERVICE_FILE=/etc/systemd/system/$SERVICE_NAME

# Disable existing service if any
sudo systemctl disable $SERVICE_NAME

# Create new startup service
{
echo "[Unit]"
echo Description=WiFi Billboard service
echo After=network-online.target
echo Wants=network-online.target
echo
echo "[Service]"
echo Type=simple
echo RemainAfterExit=yes
echo User=$USER
echo Group=$USER
echo Restart=always
echo RestartSec=10s
echo ExecStart=$PWD/run.sh
echo WorkingDirectory=$PWD
echo
echo "[Install]"
echo WantedBy=multi-user.target
} > temp.service
sudo mv temp.service $SERVICE_FILE

# Enable service
sudo systemctl enable $SERVICE_NAME
