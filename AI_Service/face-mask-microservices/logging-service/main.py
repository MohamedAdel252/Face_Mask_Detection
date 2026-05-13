from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Logging Service")

logs = []

class PredictionLog(BaseModel):
    status: str
    confidence: float
    action: str

@app.get("/")
def root():
    return {"message": "Logging Service is running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "logging-service"}

@app.post("/logs")
def add_log(log: PredictionLog):
    log_item = {
        "time": datetime.now().isoformat(),
        "status": log.status,
        "confidence": log.confidence,
        "action": log.action
    }

    logs.append(log_item)

    print("Prediction Log:", log_item)

    return {
        "message": "Log saved successfully",
        "log": log_item
    }

@app.get("/logs")
def get_logs():
    return {
        "count": len(logs),
        "logs": logs
    }