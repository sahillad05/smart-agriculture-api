from fastapi import APIRouter
from schemas.fertilizer_schema import FertilizerRecommendationRequest
from services.fertilizer_service import recommend_fertilizer

router = APIRouter()


@router.post("/fertilizer-recommendation")
def fertilizer_recommendation(request: FertilizerRecommendationRequest):

    recommendation = recommend_fertilizer(request)

    return {
        "recommended_fertilizer": recommendation
    }