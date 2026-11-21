#!/bin/bash
# Sets up and starts the frontend. Run from the project folder:  bash run_frontend.sh
cd "$(dirname "$0")/frontend" || exit 1
npm install
npm run dev
