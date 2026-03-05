# 🌾 Smart Agriculture Recommendation API

An **AI-powered REST API** that helps farmers make intelligent agricultural decisions using machine learning.

This project provides multiple machine learning services through a **FastAPI backend**, allowing users to receive recommendations and predictions related to agriculture.

---

# Project Overview

The **Smart Agriculture Recommendation API** combines machine learning models with a REST API to assist farmers with:

* Crop recommendation based on soil and climate conditions
* Fertilizer recommendation based on nutrient composition
* Crop yield prediction
* Plant disease detection from leaf images

This system is designed as a **production-style machine learning project** using modern backend and ML engineering practices.

---

# AI Systems Included

The API contains **four AI modules**:

1️⃣ Crop Recommendation System
2️⃣ Fertilizer Recommendation System
3️⃣ Crop Yield Prediction System
4️⃣ Plant Disease Detection System (Image-based CNN)

---

# Tech Stack

### Programming Language

Python

### Backend Framework

FastAPI

### Machine Learning

Scikit-learn
PyTorch

### Libraries Used

* pandas
* numpy
* scikit-learn
* joblib
* opencv-python
* pillow
* torch
* torchvision

### Deployment

* Uvicorn
* Docker

---

# Project Structure

```
smart-agriculture-api
│
├── app
│   ├── main.py
│   └── config.py
│
├── routes
│   ├── crop_routes.py
│   ├── fertilizer_routes.py
│   ├── yield_routes.py
│   └── disease_routes.py
│
├── schemas
│   ├── crop_schema.py
│   ├── fertilizer_schema.py
│   └── yield_schema.py
│
├── services
│   ├── crop_service.py
│   ├── fertilizer_service.py
│   ├── yield_service.py
│   └── disease_service.py
│
├── ml_models
│
├── ml_training
│   ├── train_crop_model.py
│   ├── train_yield_model.py
│   └── train_disease_model.py
│
├── data
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Datasets

Datasets are **not included in this repository** due to their large size.

Download them from Kaggle.

### Crop Recommendation Dataset

https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

### Crop Yield Prediction Dataset

https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset

### Plant Disease Dataset

https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset

After downloading, organize them like this:

```
data
│
├── crop_recommendation
│   └── Crop_recommendation.csv
│
├── crop_yield
│   └── crop_yield.csv
│
└── plant_disease
    └── PlantVillage
```

---

# Environment Setup

Create a conda environment:

```
conda create -n smart-agri python=3.10
```

Activate the environment:

```
conda activate smart-agri
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the API

Start the FastAPI server:

```
uvicorn app.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

Swagger UI will appear where you can test API endpoints.

---

# Machine Learning Models

The machine learning models are trained using scripts inside the `ml_training` folder.

Example:

```
python ml_training/train_crop_model.py
```

Trained models will be saved in:

```
ml_models/
```

---

# Crop Recommendation Model

This model predicts the **best crop to grow** based on soil nutrients and weather conditions.

### Input Features

* Nitrogen
* Phosphorus
* Potassium
* Temperature
* Humidity
* pH
* Rainfall

### Model Used

RandomForestClassifier

### Training Script

```
ml_training/train_crop_model.py
```

### Output Model

```
ml_models/crop_model.pkl
```

---

# Current Development Status

✔ Project setup completed
✔ FastAPI server running
✔ Crop recommendation ML model trained

Upcoming features:

* Crop recommendation API endpoint
* Yield prediction model
* Fertilizer recommendation system
* Plant disease detection CNN
* Docker deployment

---

# 👨‍💻 Author

Sahil Lad
MSc Data Science

---

# 📜 License

This project is developed for **educational and research purposes**.
