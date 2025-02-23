#!/bin/bash


# Install required packages
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed." >&2
    exit 1
fi
pip install --upgrade pip
pip install disnake
pip install google-generativeai
pip install requests
pip install Pillow
pip install python-dotenv
pip install datetime

echo "Starting Sokudo"
"$PYTHON_CMD" "$SCRIPT_DIR/main.py"