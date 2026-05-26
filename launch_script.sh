#!/bin/bash


PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"


cd "$PROJECT_DIR"
echo "Current directory : $PROJECT_DIR"

VENV="venv"
VENV_PYTHON="$PROJECT_DIR/$VENV/bin/python3"


if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV"
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r requirements.txt
fi

"$VENV_PYTHON" manual.py
