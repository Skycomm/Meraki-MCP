#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment using relative path
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "Virtual environment not found. Please create it with 'python -m venv venv' or 'uv venv'"
    exit 1
fi

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the MCP server
python meraki_server.py