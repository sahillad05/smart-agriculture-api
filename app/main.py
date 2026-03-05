from fastapi import FastAPI

app = FastAPI(
    title="Smart Agriculture Recommendation API",
    description="AI-powered API for crop recommendation, yield prediction, fertilizer suggestion, and plant disease detection.",
    version="1.0"
)

@app.get("/")
def root():
    return {
        "message": "Smart Agriculture Recommendation API is running"
    }