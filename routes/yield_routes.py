from fastapi import APIRouter
from schemas.yield_schema import YieldPredictionRequest
from services.yield_service import predict_yield

router = APIRouter()


@router.post("/yield-prediction")
def yield_prediction(request: YieldPredictionRequest):

    prediction = predict_yield(request)

    return {
        "predicted_yield": prediction
    }