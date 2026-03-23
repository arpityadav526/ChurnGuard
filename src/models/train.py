import pandas as pd
import joblib
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "IBM Teleco Churn Dataset.csv"

df = pd.read_csv(DATA_PATH)

# -------------------
# BASIC PREPROCESSING
# -------------------
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

if "customerID" in df.columns:
    df = df.drop("customerID", axis=1)


# Target
y = df["Churn"].map({"Yes": 1, "No": 0})
X = df.drop("Churn", axis=1)

# One-hot encoding
X_encoded = pd.get_dummies(X)

# -------------------
# TRAIN-TEST SPLIT
# -------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

# -------------------
# HANDLE IMBALANCE
# -------------------
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.08,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric="logloss"
)


model.fit(X_train, y_train)

# -------------------
# PREDICTIONS
# -------------------
y_prob = model.predict_proba(X_test)[:, 1]

# threshold can be tuned later
threshold = 0.4
y_pred = (y_prob >= threshold).astype(int)

# -------------------
# METRICS
# -------------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
    "roc_auc": float(roc_auc),
    "confusion_matrix": {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    },
}

# -------------------
# SAVE FILES
# -------------------
MODEL_PATH = BASE_DIR / "src" / "models" / "churn_model.pkl"
COLUMNS_PATH = BASE_DIR / "src" / "models" / "model_columns.pkl"
METRICS_PATH = BASE_DIR / "src" / "models" / "model_metrics.pkl"

joblib.dump(model, MODEL_PATH)
joblib.dump(X_encoded.columns.tolist(), COLUMNS_PATH)
joblib.dump(metrics, METRICS_PATH)

print("Model saved successfully.")
print("Metrics:")
print(metrics)
print("Accuracy:", accuracy)
print("ROC-AUC:", roc_auc)
print("Precision:", precision)
print("Recall:", recall)