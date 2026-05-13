from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")

class Prediction(BaseModel):
    status: str
    confidence: float
    action: str

@app.get("/")
def root():
    return {"message": "Notification Service is running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}

@app.post("/notify")
def notify(prediction: Prediction):
    if prediction.status == "without_mask":
        print("🚨 ALERT: Person without mask detected!")
        return {
            "alert": True,
            "message": "No mask detected - action required!"
        }

    return {
        "alert": False,
        "message": "All good - mask detected"
    }