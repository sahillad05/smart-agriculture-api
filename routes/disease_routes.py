from fastapi import APIRouter, UploadFile, File
from PIL import Image
from services.disease_service import predict_disease

router = APIRouter()


@router.post("/disease-detection")
async def detect_disease(file: UploadFile = File(...)):

    image = Image.open(file.file).convert("RGB")

    disease, confidence = predict_disease(image)

    return {
        "disease": disease,
        "confidence": round(confidence, 3)
    }