from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crop_router)
app.include_router(yield_router)
app.include_router(fertilizer_router)
app.include_router(disease_router)

# Mount frontend directory to root to serve index.html, CSS, and JS natively
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")