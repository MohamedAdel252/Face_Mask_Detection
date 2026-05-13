from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import io

app = FastAPI(title="Image Service")

@app.get("/")
def root():
    return {"message": "Image Service is running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "image-service"}

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        width, height = image.size

        return {
            "message": "Image processed successfully",
            "width": width,
            "height": height
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")