# Disease Prediction (React + Flask + Scikit-learn)

Select symptoms -> the app predicts a likely disease and shows its description and
precautions. For learning only, NOT medical advice.

## How to run (Mac)

Open TWO terminals in this folder.

Terminal 1 (backend):
    conda deactivate        # only if you see (base) in your prompt; run it until (base) is gone
    bash run_backend.sh

Terminal 2 (frontend):
    bash run_frontend.sh

Then open http://localhost:5173

The first run takes 2-3 minutes (it installs packages and trains the model).
Backend runs on port 5001, frontend on 5173.

## Check the backend
    curl http://localhost:5001/health      ->  {"status":"ok"}

## Folder structure
    backend/train_model.py   cleans data, compares 3 models, saves Random Forest
    backend/app.py           Flask API: /symptoms and /predict
    backend/data/            Training.csv + description and precaution files
    frontend/src/App.jsx     the whole React UI

Live demo: https://health-sense-ai-wine.vercel.app/

A web app that predicts a likely disease from selected symptoms and shows
its description and precautions. For learning only, not medical advice.
   
