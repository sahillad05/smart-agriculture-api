from pydantic import BaseModel

class FertilizerRecommendationRequest(BaseModel):

    crop: str
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_type: str