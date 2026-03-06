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

---

## Crop Recommendation API

The crop recommendation API predicts the most suitable crop based on soil nutrients and environmental conditions.

Endpoint

POST /crop-recommendation

Input Parameters

* nitrogen
* phosphorus
* potassium
* temperature
* humidity
* ph
* rainfall

Example Request

{
"nitrogen": 90,
"phosphorus": 42,
"potassium": 43,
"temperature": 20,
"humidity": 82,
"ph": 6.5,
"rainfall": 202
}

Example Response

{
"recommended_crop": "rice"
}

Model Used

RandomForestClassifier trained on the Crop Recommendation Dataset.

The model is stored at:

ml_models/crop_model.pkl

---

## Crop Yield Prediction Model

The crop yield prediction system estimates agricultural productivity based on environmental and regional factors.

This model helps estimate the expected crop yield per hectare using historical agricultural data.

### Dataset

The dataset used for training contains the following columns:

Area
Item
Year
hg/ha_yield
average_rain_fall_mm_per_year
pesticides_tonnes
avg_temp

### Feature Engineering

For model training, the dataset columns are processed as follows:

Area → Encoded using LabelEncoder
Item → Encoded using LabelEncoder

Selected features:

Area
Crop
Rainfall
Pesticides
Temperature

Target variable:

Yield (hg/ha_yield)

### Machine Learning Model

RandomForestRegressor from scikit-learn is used for regression.

This model is well suited for tabular datasets and handles nonlinear relationships effectively.

### Training Script

The model is trained using the script:

ml_training/train_yield_model.py

Run the training script using:

python ml_training/train_yield_model.py

### Output Files

After training, the following files are generated inside the `ml_models` directory:

ml_models/yield_model.pkl
ml_models/area_encoder.pkl
ml_models/crop_encoder.pkl

These files are used by the FastAPI backend to perform yield prediction.

### Evaluation Metric

The model performance is evaluated using Root Mean Squared Error (RMSE).

---

## Fertilizer Recommendation API

The fertilizer recommendation API suggests the most suitable fertilizer based on soil nutrient composition and crop type.

Endpoint

POST /fertilizer-recommendation

Input Parameters

crop
nitrogen
phosphorus
potassium
soil_type

Example Request

{
"crop": "Wheat",
"nitrogen": 30,
"phosphorus": 50,
"potassium": 40,
"soil_type": "Loamy"
}

Example Response

{
"recommended_fertilizer": "Urea"
}

Recommendation Logic

The system uses rule-based logic to detect nutrient deficiencies in soil and suggest an appropriate fertilizer.

---

## Plant Disease Detection Model

The plant disease detection module uses a convolutional neural network built with PyTorch to classify plant diseases from leaf images.

Dataset

The dataset is organized using the following structure:

data/plant_disease/dataset/train
data/plant_disease/dataset/valid

Each disease category is stored inside its own folder.

Example

train/Apple___Apple_scab
train/Tomato___Early_blight

Model Architecture

Custom Convolutional Neural Network (CNN) implemented using PyTorch.

Training Configuration

Image Size: 128x128
Batch Size: 16
Epochs: 15
Device: GPU (CUDA)

Training Script

ml_training/train_disease_model.py

Model Output

ml_models/disease_model.pth

Checkpoint File

ml_models/disease_checkpoint.pth

The checkpoint file allows training to resume if the training process is interrupted.

Validation Accuracy

The trained model achieved approximately 94 percent validation accuracy on the dataset.


---

## Plant Disease Detection API

The disease detection API allows users to upload a plant leaf image and receive a predicted disease class using the trained CNN model.

Endpoint

POST /disease-detection

Input

Multipart image upload of a plant leaf.

Example Request

Upload an image file using Swagger UI or an HTTP client.

Example Response

{
"disease": "Tomato___Early_blight",
"confidence": 0.94
}

Model Used

Custom Convolutional Neural Network trained using PyTorch.

Image Processing

Images are resized to 128x128 and converted to tensors before being passed into the CNN model.

Model File

ml_models/disease_model.pth

Supported Classes

Apple___Apple_scab
Apple___Black_rot
Apple___healthy
Corn_(maize)__*Northern_Leaf_Blight
Corn*(maize)___healthy
Potato___Early_blight
Potato___Late_blight
Potato___healthy
Tomato___Early_blight
Tomato___Late_blight
Tomato___Septoria_leaf_spot
Tomato___Target_Spot
Tomato___Tomato_Yellow_Leaf_Curl_Virus
Tomato___healthy


---

## Deployment

The Smart Agriculture Recommendation API can be deployed using Docker.

Docker Build

docker build -t smart-agriculture-api .

Docker Run

docker run -p 8000:8000 smart-agriculture-api

Access API

http://localhost:8000/docs

Cloud Deployment

The API can be deployed on cloud platforms such as Render.

Steps

1. Push project to GitHub
2. Connect repository to Render
3. Deploy as a Web Service using Docker
4. Access API documentation via /docs endpoint

---

# 👨‍💻 Author

Sahil Lad
MSc Data Science

---

# 📜 License

This project is developed for **educational and research purposes**.
