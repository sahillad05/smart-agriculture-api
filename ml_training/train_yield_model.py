import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder


# -------------------------
# Load Dataset
# -------------------------

data_path = "data/crop_yield/yield_data.csv"

df = pd.read_csv(data_path)

print("Dataset Loaded")
print(df.head())
print(df.columns)

# -------------------------
# Rename columns (optional for clean code)
# -------------------------

df = df.rename(columns={
    "Item": "Crop",
    "hg/ha_yield": "Yield",
    "average_rain_fall_mm_per_year": "Rainfall",
    "pesticides_tonnes": "Pesticides",
    "avg_temp": "Temperature"
})


# -------------------------
# Encode Categorical Columns
# -------------------------

area_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df["Area"] = area_encoder.fit_transform(df["Area"])
df["Crop"] = crop_encoder.fit_transform(df["Crop"])


# -------------------------
# Feature Selection
# -------------------------

X = df[[
    "Area",
    "Crop",
    "Rainfall",
    "Pesticides",
    "Temperature"
]]

y = df["Yield"]


# -------------------------
# Train Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -------------------------
# Train Model
# -------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# -------------------------
# Evaluate Model
# -------------------------

y_pred = model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred, squared=False)

print("RMSE:", rmse)


# -------------------------
# Save Model + Encoders
# -------------------------

joblib.dump(model, "ml_models/yield_model.pkl")
joblib.dump(area_encoder, "ml_models/area_encoder.pkl")
joblib.dump(crop_encoder, "ml_models/crop_encoder.pkl")

print("Models saved in ml_models/")