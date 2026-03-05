import joblib
import numpy as np

MODEL_PATH = "ml_models/crop_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_crop(data):

    features = np.array([[
        data.nitrogen,
        data.phosphorus,
        data.potassium,
        data.temperature,
        data.humidity,
        data.ph,
        data.rainfall
    ]])

    prediction = model.predict(features)

    return prediction[0]