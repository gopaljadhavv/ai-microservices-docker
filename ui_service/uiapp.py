from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from pathlib import Path
import os
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a FastAPI app with custom title and description
app = FastAPI(
    title="Image Detection API",
    description="API for uploading images and detecting objects using YOLO model.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8000/detect")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def home():
    return templates.TemplateResponse("upload.html", {"request": {}})

@app.post("/upload/")
async def upload(file: UploadFile):
    """
    Upload an image for detection.

    - **file**: The image file to be uploaded. Supported formats: JPEG, PNG, GIF.
    
    Returns a JSON response containing:
    - **image**: Base64 encoded image with detections.
    - **objects**: List of detected objects with their properties.
    - **count**: Number of detected objects.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")
    
    if file.size > 5 * 1024 * 1024:  # Limit to 5 MB
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 5 MB.")
    
    try:
        # Read the file and encode it in Base64
        contents = await file.read()
        encoded_image = base64.b64encode(contents).decode('utf-8')

        # Send the encoded image to the AI service
        response = requests.post(AI_SERVICE_URL, json={"image": encoded_image})
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with AI service: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service.")
    
    return response.json()
