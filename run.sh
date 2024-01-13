#!/bin/bash

SCRIPT_RELATIVE_PATH=$(dirname "$0")
SCRIPT_FULL_PATH="$(realpath -s $0)"
SCRIPT_DIR="$(dirname $SCRIPT_FULL_PATH)"

cd $SCRIPT_DIR
sudo uvicorn wifi_billboard:app --host 0.0.0.0 --port 80
