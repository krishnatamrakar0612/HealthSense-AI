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

## Use the real Kaggle dataset
1. Download "Disease Prediction Using Machine Learning" from Kaggle.
2. Replace these 3 files inside backend/data/ :
   Training.csv, symptom_Description.csv, symptom_precaution.csv
3. Delete backend/models/model.pkl, then run: bash run_backend.sh
   (it trains again and prints the real accuracy and duplicate count)
