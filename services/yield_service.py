import joblib
import numpy as np


# Load model and encoders
model = joblib.load("ml_models/yield_model.pkl")

area_encoder = joblib.load("ml_models/area_encoder.pkl")
crop_encoder = joblib.load("ml_models/crop_encoder.pkl")


def predict_yield(data):

    area_encoded = area_encoder.transform([data.area])[0]
    crop_encoded = crop_encoder.transform([data.crop])[0]

    features = np.array([[
        area_encoded,
        crop_encoded,
        data.rainfall,
        data.pesticides,
        data.temperature
    ]])

    prediction = model.predict(features)

    return float(prediction[0])