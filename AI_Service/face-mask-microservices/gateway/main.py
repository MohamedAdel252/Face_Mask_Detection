import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Face Mask API Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)	

PREDICTION_SERVICE_URL = "http://prediction-service:8001/predict"
LOGGING_SERVICE_URL = "http://logging-service:8003/logs"
NOTIFICATION_SERVICE_URL = "http://notification-service:8004/notify"

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Face Mask Detection Gateway</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #0f172a;
                    color: white;
                    text-align: center;
                    padding-top: 80px;
                }
                .card {
                    width: 600px;
                    margin: auto;
                    padding: 30px;
                    border-radius: 20px;
                    background: #111827;
                    box-shadow: 0 0 30px rgba(0,0,0,0.4);
                }
                h1 { color: #38bdf8; }
                .badge {
                    display: inline-block;
                    margin-top: 15px;
                    padding: 10px 18px;
                    border-radius: 999px;
                    background: #2563eb;
                    font-weight: bold;
                }
                .services {
                    margin-top: 25px;
                    text-align: left;
                    line-height: 1.8;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Face Mask Detection System</h1>
                <p>Containerized Microservices Architecture</p>
                <div class="badge">Powered by Docker</div>

                <div class="services">
                    <p>✅ API Gateway</p>
                    <p>✅ Prediction Service</p>
                    <p>✅ Logging Service</p>
                    <p>✅ Notification Service</p>
                    <p>✅ RabbitMQ</p>
                </div>

                <p>
					<a style="color:#38bdf8; margin-right:20px;" href="http://localhost:8080">
						Open Frontend Demo
					</a>

					<a style="color:#38bdf8" href="/docs">
						Open Swagger Docs
					</a>
					</p>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "gateway",
        "architecture": "microservices",
        "powered_by": "Docker"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        files = {
            "file": (file.filename, image_bytes, file.content_type)
        }

        prediction_response = requests.post(
            PREDICTION_SERVICE_URL,
            files=files,
            timeout=30
        )

        if prediction_response.status_code != 200:
            raise HTTPException(
                status_code=prediction_response.status_code,
                detail=prediction_response.text
            )

        prediction_result = prediction_response.json()

        try:
            requests.post(LOGGING_SERVICE_URL, json=prediction_result, timeout=5)
        except Exception:
            print("Logging service unavailable")

        try:
            notification_response = requests.post(
                NOTIFICATION_SERVICE_URL,
                json=prediction_result,
                timeout=5
            )
            notification_result = notification_response.json()
        except Exception:
            notification_result = {
                "alert": False,
                "message": "Notification service unavailable"
            }

        return {
            "prediction": prediction_result,
            "notification": notification_result,
            "system": {
                "gateway": "active",
                "powered_by": "Docker",
                "architecture": "microservices"
            }
        }

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Prediction service is unavailable")