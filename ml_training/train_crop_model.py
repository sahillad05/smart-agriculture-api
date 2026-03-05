import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# 1 Load Dataset
# -----------------------------

data_path = "data/crop_recommendation/Crop_recommendation.csv"

df = pd.read_csv(data_path)

print("Dataset Loaded Successfully")
print(df.head())


# -----------------------------
# 2 Feature Selection
# -----------------------------

X = df.drop("label", axis=1)
y = df["label"]


# -----------------------------
# 3 Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------
# 4 Train Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# -----------------------------
# 5 Evaluate Model
# -----------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# -----------------------------
# 6 Save Model
# -----------------------------

model_path = "ml_models/crop_model.pkl"

joblib.dump(model, model_path)

print("\nModel Saved at:", model_path)