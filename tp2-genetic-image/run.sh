#!/bin/bash
# Creates a virtual environment if it doesn't exist, installs dependencies, and runs the program.
# Usage: ./run.sh --image inputs/example.png --triangles 50

set -e

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet

python main.py "$@"
