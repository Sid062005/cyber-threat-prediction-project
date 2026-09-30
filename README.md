# Cyber Threat Prediction System

## Project
Machine-learning based network threat prediction using UNSW-NB15.

## Stack
Python, Pandas, Scikit-learn, Random Forest, Flask, HTML/CSS, Joblib.

## Dataset
Use the official UNSW-NB15 training/test CSV files. The project supports a CSV with `attack_cat` for multiclass prediction or `label` for binary prediction.

## Run
1. Create environment:
   `python -m venv venv`
2. Activate it and install:
   `pip install -r requirements.txt`
3. Train:
   `python train_model.py --csv path/to/UNSW_NB15_training-set.csv --target attack_cat`
4. Start dashboard:
   `python app.py`
5. Open the Flask address shown in the terminal.
6. Upload a compatible CSV for batch prediction.

## Demo-only pipeline
`python demo_gen.py`
Then train with:
`python train_model.py --csv demo_data.csv --target attack_cat`

Do not report demo-data accuracy as research results. Replace it with results from UNSW-NB15.

## Suggested report result table
Fill these from the training output:
Accuracy: ______
Precision: ______
Recall: ______
F1-score: ______

## Important academic note
The model predicts patterns learned from the selected dataset. It is a prototype decision-support/IDS component, not a guarantee that an unseen real-world attack will be detected.
