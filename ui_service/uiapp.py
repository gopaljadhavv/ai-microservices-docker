from fastapi import FastAPI, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from pathlib import Path
import os
import base64
import logging
import json
from pydantic import BaseModel
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI app with custom title and description
app = FastAPI(
    title="Image Detection UI Service",
    description="Web interface for uploading images and detecting objects using YOLO model.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai_service:8000/detect")

# Pydantic models for save results
class SaveRequest(BaseModel):
    result: Dict[str, Any]
    filename: str

class SaveResponse(BaseModel):
    success: bool
    files: List[str]
    message: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ui_service"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

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
    try:
        # Validate file type
        if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/jpg"]:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only JPEG, PNG, and GIF are allowed."
            )
        
        # Validate file size (5MB limit)
        if file.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400, 
                detail="File size exceeds the limit of 5 MB."
            )
        
        logger.info(f"Processing file: {file.filename}, size: {file.size} bytes")
        
        # Read the file and encode it in Base64
        contents = await file.read()
        encoded_image = base64.b64encode(contents).decode('utf-8')

        # Send the encoded image to the AI service
        payload = {"image": encoded_image,
        "image_path": file.filename}
        response = requests.post(AI_SERVICE_URL, json=payload, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"AI service returned error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"AI service error: {response.text}"
            )
        
        result = response.json()
        logger.info(f"Detection completed successfully. Found {result.get('count', 0)} objects")
        
        # The AI service now returns the filename, so we don't need to add it here
        return JSONResponse(content=result)
        
    except requests.exceptions.Timeout:
        logger.error("Timeout while communicating with AI service")
        raise HTTPException(status_code=504, detail="Request timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error with AI service")
        raise HTTPException(status_code=503, detail="AI service is unavailable. Please try again later.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with AI service: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.post("/save-results/", response_model=SaveResponse)
async def save_results(request: SaveRequest):
    """
    Save detection results to demo_outputs directory.
    
    - **result**: The detection result object
    - **filename**: Original filename (without extension)
    
    Returns information about saved files.
    """
    try:
        # Create demo_outputs directory if it doesn't exist
        demo_outputs_dir = Path("../demo_outputs")
        demo_outputs_dir.mkdir(exist_ok=True)
        
        # Generate base filename from original filename
        base_filename = Path(request.filename).stem
        if not base_filename or base_filename == "detection":
            import time
            base_filename = f"detection_{int(time.time())}"
        
        saved_files = []
        
        # Save JSON results
        original_filename = Path(request.filename)
        json_filename = f"{original_filename.stem}_results.json"
        json_path = demo_outputs_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(request.result, f, indent=2, ensure_ascii=False)
        
        saved_files.append(json_filename)
        logger.info(f"Saved JSON results to: {json_path}")
        
        # Save image with bounding boxes
        if 'image' in request.result and request.result['image']:
            try:
                image_data = base64.b64decode(request.result['image'])
                # Use original filename with "_detected" suffix
                original_filename = Path(request.filename)
                image_filename = f"{original_filename.stem}_detected{original_filename.suffix}"
                image_path = demo_outputs_dir / image_filename
                
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                
                saved_files.append(image_filename)
                logger.info(f"Saved detected image to: {image_path}")
            except Exception as e:
                logger.error(f"Error saving image: {e}")
        
        return SaveResponse(
            success=True,
            files=saved_files,
            message=f"Successfully saved {len(saved_files)} files to demo_outputs directory"
        )
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving results: {str(e)}")

@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    try:
        # Check AI service health
        ai_health = requests.get(AI_SERVICE_URL.replace("/detect", "/health"), timeout=5)
        ai_status = "healthy" if ai_health.status_code == 200 else "unhealthy"
    except:
        ai_status = "unreachable"
    
    return {
        "ui_service": "healthy",
        "ai_service": ai_status,
        "ai_service_url": AI_SERVICE_URL
    }

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "service": "Image Detection UI Service",
        "version": "1.0.0",
        "ai_service_url": AI_SERVICE_URL,
        "supported_formats": ["JPEG", "PNG", "GIF"],
        "max_file_size": "5MB"
    }
