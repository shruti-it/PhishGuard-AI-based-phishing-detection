import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle, json

data = pd.read_csv("dataset.csv")
X = data.drop("Result", axis=1)
y = data["Result"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "XGBoost": XGBClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Logistic Regression": LogisticRegression(max_iter=1000)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    results[name] = {
        "accuracy": round(accuracy_score(y_test, pred)*100, 2),
        "precision": round(precision_score(y_test, pred, average='weighted', zero_division=0)*100, 2),
        "recall": round(recall_score(y_test, pred, average='weighted', zero_division=0)*100, 2),
        "f1": round(f1_score(y_test, pred, average='weighted', zero_division=0)*100, 2)
    }
    print(name, results[name])

# Save best model (XGBoost) + results
pickle.dump(models["XGBoost"], open("model.pkl","wb"))
json.dump(results, open("metrics.json","w"), indent=4)
print("Saved model.pkl + metrics.json")
