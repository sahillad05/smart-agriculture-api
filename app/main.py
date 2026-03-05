from fastapi import FastAPI

from routes.crop_routes import router as crop_router

app = FastAPI(
    title="Smart Agriculture Recommendation API",
    description="AI powered API for agricultural recommendations",
    version="1.0"
)

app.include_router(crop_router)


@app.get("/")
def root():
    return {"message": "Smart Agriculture Recommendation API is running"}