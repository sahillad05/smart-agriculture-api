import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

data_path = "data/crop_recommendation/Crop_recommendation.csv"
model_path = "ml_models/crop_model.pkl"

def evaluate_crop_model():
    print("Evaluating Crop Recommendation Model...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Dataset not found at {data_path}")
        return

    X = df.drop("label", axis=1)
    y = df["label"]
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: Model not found at {model_path}")
        return
        
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate_crop_model()
