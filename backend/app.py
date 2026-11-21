"""
Flask API.
  GET  /health    -> check the server is running
  GET  /symptoms  -> list of symptoms the model knows
  POST /predict   -> body: {"symptoms": ["itching", "skin_rash"]}
"""
import os
import re
import pickle
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Which website addresses may call this API (CORS).
# Locally: the Vite dev server. When deployed: set FRONTEND_URL to your Vercel address.
allowed = os.environ.get("FRONTEND_URL", "http://localhost:5173,http://127.0.0.1:5173")
origins = [o.strip().rstrip("/") for o in allowed.split(",") if o.strip()]
CORS(app, origins=origins)


def clean(text):
    return re.sub(r"\s+", " ", str(text)).strip()


# Load the model ONCE when the server starts
with open("models/model.pkl", "rb") as f:
    saved = pickle.load(f)
model = saved["model"]
label_encoder = saved["label_encoder"]
symptom_list = saved["symptoms"]

# Load description and precaution files
desc_df = pd.read_csv("data/symptom_Description.csv")
prec_df = pd.read_csv("data/symptom_precaution.csv")
desc_df["Disease"] = desc_df["Disease"].map(clean)
prec_df["Disease"] = prec_df["Disease"].map(clean)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/symptoms")
def symptoms():
    return jsonify(symptom_list)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    selected = data.get("symptoms", [])

    if len(selected) == 0:
        return jsonify({"error": "Please select at least one symptom."}), 400

    # Turn the symptoms into 0s and 1s, in the same order used for training
    row = pd.DataFrame([[1 if s in selected else 0 for s in symptom_list]],
                       columns=symptom_list)

    # Predict: the model gives a number, we convert it back to the disease name
    prediction = model.predict(row)[0]
    disease = label_encoder.inverse_transform([prediction])[0]

    # Look up the description
    desc = desc_df.loc[desc_df["Disease"] == disease, "Description"]
    description = desc.values[0] if len(desc) > 0 else "No description available."

    # Look up the precautions
    precautions = []
    prec = prec_df.loc[prec_df["Disease"] == disease]
    if len(prec) > 0:
        precautions = [p for p in prec.iloc[0, 1:].tolist() if isinstance(p, str)]

    return jsonify({
        "disease": disease,
        "description": description,
        "precautions": precautions,
    })


if __name__ == "__main__":
    # Locally this runs on port 5001. On Render, gunicorn starts the app instead.
    app.run(port=int(os.environ.get("PORT", 5001)))