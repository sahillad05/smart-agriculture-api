from fastapi import FastAPI

from services.model_loader import download_models

from routes.crop_routes import router as crop_router
from routes.yield_routes import router as yield_router
from routes.fertilizer_routes import router as fertilizer_router
from routes.disease_routes import router as disease_router

download_models()

app = FastAPI(
    title="Smart Agriculture Recommendation API",
    description="AI powered API for agricultural recommendations",
    version="1.0"
)

app.include_router(crop_router)
app.include_router(yield_router)
app.include_router(fertilizer_router)
app.include_router(disease_router)


@app.get("/")
def root():
    return {"message": "Smart Agriculture Recommendation API is running"}