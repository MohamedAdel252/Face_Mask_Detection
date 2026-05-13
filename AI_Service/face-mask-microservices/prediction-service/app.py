import io
import json
from pathlib import Path

import torch
import torch.nn as nn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from torchvision import transforms, models

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "mask_detector_cpu.pth"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

device = torch.device("cpu")
torch.set_num_threads(1)	

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

model = models.mobilenet_v2(weights=None)
in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, len(class_names))

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

app = FastAPI(title="Face Mask Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_action(predicted_class: str):
    if predicted_class == "with_mask":
        return "Allow entry"
    return "Deny entry"

@app.get("/")
def root():
    return {"message": "Face Mask Detection API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")

    try:
        tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(tensor)
            probs = torch.softmax(outputs, dim=1)[0]
            pred_idx = probs.argmax().item()

        predicted_class = class_names[pred_idx]
        confidence = float(probs[pred_idx]) * 100

        return {
            "status": predicted_class,
            "confidence": round(confidence, 2),
            "action": get_action(predicted_class)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)