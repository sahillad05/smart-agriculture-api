from pydantic import BaseModel

class YieldPredictionRequest(BaseModel):

    area: str
    crop: str
    rainfall: float
    pesticides: float
    temperature: float