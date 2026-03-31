#!/bin/bash

# Direcories
PROJECT_DIR=$(pwd)
VENV="venv"
VENV_PYTHON="$PROJECT_DIR/$VENV/bin/python3"


cd "$PROJECT_DIR"
echo "Current directory : ${Project_DIR}"

if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment"
    python3 -m venv "$VENV"
    "$VENV_PYTHON" -m pip install -r requirements.txt
fi

"$VENV_PYTHON" manual.py