# AI Based Phishing Detection

Detects whether a website URL is Phishing (Fake) or Legitimate using Machine Learning. This helps protect users from fake login pages, scams, and data theft.

## Dataset
- `dataset.csv` - Phishing Website Dataset
- Features: URL Length, Having IP Address, HTTPS, Domain Age, Having @ Symbol, etc.
- Target: Phishing (1 = Phishing, 0 = Legitimate)

## What I Did
- Data Creation - Created dataset using `make_dataset.py`
- Feature Engineering - Extracted 20+ features from URLs using `features.py`
- Model Training - Trained model using `train.py`
- Web App - Built interactive web app using Flask + HTML
- Model Evaluation - Accuracy, Precision, Recall, Confusion Matrix

## Files in this Project
- `app.py` - Main Flask app, runs the website
- `train.py` - Trains the Machine Learning model
- `make_dataset.py` - Creates / prepares the dataset
- `features.py` - Extracts features from URLs
- `dataset.csv` - Dataset used for training
- `index.html` - Home page - Check single URL
- `result.html` - Shows prediction result
- `detail.html` - Shows detailed feature analysis of URL
- `bulk.html` - Check multiple URLs at once

## Tech Stack
Python, Pandas, NumPy, Scikit-learn, Flask, HTML, CSS

## How to Run
pip install -r requirements.txt
python train.py
python app.py

Then open in browser: http://127.0.0.1:5000

## Features of App
- Single URL Check
- Bulk URL Check
- Detailed Feature Explanation
- Real-time Prediction

## Result
Model can detect phishing websites with high accuracy and helps users browse safely.
