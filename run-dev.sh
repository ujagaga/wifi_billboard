#!/bin/bash

SCRIPT_RELATIVE_PATH=$(dirname "$0")
SCRIPT_FULL_PATH="$(realpath -s $0)"
SCRIPT_DIR="$(dirname $SCRIPT_FULL_PATH)"

cd $SCRIPT_DIR
uvicorn wifi_billboard:app --reload
