from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import joblib
import os
import json

from huggingface_hub import hf_hub_download


app = Flask(__name__)
app.secret_key = "college-demo-key"

# ============================================================
# Hugging Face model repository
# ============================================================

HF_REPO_ID = "Siddharth1102/cyber-threat-model"

MODEL_FILENAME = "cyber_threat_model_deploy.joblib"
META_FILENAME = "model_meta.json"


# ============================================================
# Download model from Hugging Face
# ============================================================

try:
    MODEL_PATH = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=MODEL_FILENAME,
        repo_type="model"
    )

    META_PATH = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=META_FILENAME,
        repo_type="model"
    )

    model = joblib.load(MODEL_PATH)

    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    print("Model loaded successfully.")
    print("Model path:", MODEL_PATH)

except Exception as e:
    print("ERROR loading model:")
    print(e)

    model = None
    meta = {}


# ============================================================
# Home page
# ============================================================

@app.route("/")
def index():
    return render_template(
        "index.html",
        model_ready=model is not None,
        classes=meta.get("classes", [])
    )


# ============================================================
# Prediction
# ============================================================

@app.post("/predict")
def predict():

    if model is None:
        flash("Model could not be loaded.")
        return redirect(url_for("index"))

    f = request.files.get("file")

    if not f or not f.filename.lower().endswith(".csv"):
        flash("Please upload a CSV file.")
        return redirect(url_for("index"))

    try:

        df = pd.read_csv(f)

        original = df.copy()

        # Remove target columns if they exist
        drop = [
            c for c in ["attack_cat", "label"]
            if c in df.columns
        ]

        X = df.drop(
            columns=drop,
            errors="ignore"
        )

        # Predict
        preds = model.predict(X)

        original["Predicted_Threat"] = preds

        # Threat distribution
        counts = (
            original["Predicted_Threat"]
            .value_counts()
            .to_dict()
        )

        # Display first 100 rows
        html_table = original.head(100).to_html(
            classes="table",
            index=False
        )

        return render_template(
            "results.html",
            table=html_table,
            counts=counts,
            rows=len(original)
        )

    except Exception as e:

        flash(
            "Prediction error: " + str(e)
        )

        return redirect(
            url_for("index")
        )


# ============================================================
# Run application
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                7860
            )
        )
    )