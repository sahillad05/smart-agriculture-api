from fastapi import APIRouter
from schemas.crop_schema import CropRecommendationRequest
from services.crop_service import predict_crop

router = APIRouter()

@router.post("/crop-recommendation")
def crop_recommendation(request: CropRecommendationRequest):

    prediction = predict_crop(request)

    return {
        "recommended_crop": prediction
    }