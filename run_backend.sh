#!/bin/bash
# Sets up and starts the backend. Run from the project folder:  bash run_backend.sh
cd "$(dirname "$0")/backend" || exit 1

if [ ! -d venv ]; then
  python3 -m venv venv
fi

./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt

if [ ! -f models/model.pkl ]; then
  ./venv/bin/python train_model.py
fi

echo "Starting backend on http://localhost:5001 ..."
./venv/bin/python app.py
