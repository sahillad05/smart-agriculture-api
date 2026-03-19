import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

data_path = "data/crop_yield/yield_data.csv"
model_path = "ml_models/yield_model.pkl"
area_enc_path = "ml_models/area_encoder.pkl"
crop_enc_path = "ml_models/crop_encoder.pkl"

def evaluate_yield_model():
    print("Evaluating Crop Yield Prediction Model...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Dataset not found at {data_path}")
        return

    df = df.rename(columns={
        "Item": "Crop",
        "hg/ha_yield": "Yield",
        "average_rain_fall_mm_per_year": "Rainfall",
        "pesticides_tonnes": "Pesticides",
        "avg_temp": "Temperature"
    })

    try:
        area_encoder = joblib.load(area_enc_path)
        crop_encoder = joblib.load(crop_enc_path)
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: Models/Encoders not found in ml_models/")
        return

    # To avoid unseen labels warning, we only evaluate on standard set 
    # Or just use the already fitted encoder
    df["Area"] = area_encoder.transform(df["Area"])
    df["Crop"] = crop_encoder.transform(df["Crop"])

    X = df[["Area", "Crop", "Rainfall", "Pesticides", "Temperature"]]
    y = df["Yield"]
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
    y_pred = model.predict(X_test)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nRoot Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R-squared (R2) Score: {r2:.4f}")

if __name__ == "__main__":
    evaluate_yield_model()
