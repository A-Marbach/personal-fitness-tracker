
from fastapi import FastAPI

from app.api.weights import router as weights_router
from app.api.workouts import router as workouts_router


app = FastAPI(
    title="Personal Fitness Tracker API",
    version="0.1.0",
)

app.include_router(weights_router)
app.include_router(workouts_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
