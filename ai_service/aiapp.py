import base64
import os
import io
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel
from typing import List
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Pydantic models
class DetectionResult(BaseModel):
    label: str
    x: int
    y: int
    width: int
    height: int
    confidence: float

class DetectRequest(BaseModel):
    image: str  # Base64 encoded image
    image_path: str = None  # Optional image path for reference

class DetectResponse(BaseModel):
    filename: str = None  # Original filename
    objects: List[DetectionResult]
    count: int
    image: str  # Base64 encoded image with detections

# Global variable for model
model = None

def load_model():
    """Load the YOLO model"""
    global model
    try:
        model_path = './models/yolov8n.onnx'
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        model = YOLO(model_path,)
        logger.info("YOLO model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model
    model = load_model()
    logger.info("AI service started successfully")
    yield
    # Shutdown
    logger.info("AI service shutting down")

app = FastAPI(
    title="AI Object Detection Service",
    description="Detecting objects in images using YOLOv8 Nano model with bounding boxes.",
    version="1.0.0",
    lifespan=lifespan
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai_object_detection"}

def draw_bounding_boxes(image, results):
    """Draw bounding boxes on the image"""
    try:
        # Convert PIL image to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Draw bounding boxes
        for r in results:
            if r.boxes is not None:
                for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
                    x1, y1, x2, y2 = box.tolist()
                    label = r.names[int(cls)]
                    confidence = float(conf)
                    
                    # Draw rectangle
                    cv2.rectangle(img_cv, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Add label
                    label_text = f"{label}: {confidence:.2f}"
                    cv2.putText(img_cv, label_text, (int(x1), int(y1) - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Convert back to PIL
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)
    except Exception as e:
        logger.error(f"Error drawing bounding boxes: {e}")
        return image

# POST router for object detection
@app.post("/detect/", response_model=DetectResponse)
async def detect_objects(request: DetectRequest):
    """Handles POST requests to /detect/ endpoint for object detection."""
    try:
        encoded_image = request.image
        image_path = request.image_path

        if not encoded_image:
            raise HTTPException(status_code=400, detail="No image provided.")

        # Decode the Base64 image
        image_data = base64.b64decode(encoded_image)
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        logger.info(f"Processing image of size: {img.size}")

        # Perform object detection
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")

        results = model(img, conf=0.5)
        
        # Process object detection results
        output = []
        for r in results:
            if r.boxes is not None:
                for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
                    x1, y1, x2, y2 = box.tolist()
                    detected_label = r.names[int(cls)]
                    confidence = float(conf)
                    
                    entry = DetectionResult(
                        label=detected_label,
                        x=int(x1),
                        y=int(y1),
                        width=int(x2 - x1),
                        height=int(y2 - y1),
                        confidence=round(confidence, 3)
                    )
                    output.append(entry)

        # Draw bounding boxes on the image
        img_with_boxes = draw_bounding_boxes(img, results)

        # Encode the image with bounding boxes to Base64
        buffered = io.BytesIO()
        img_with_boxes.save(buffered, format="JPEG", quality=95)
        encoded_image_with_boxes = base64.b64encode(buffered.getvalue()).decode('utf-8')

        logger.info(f"Detection completed. Found {len(output)} objects")

        # Return the results
        return DetectResponse(
            filename=image_path,
            objects=output,
            count=len(output),
            image=encoded_image_with_boxes,
        )
        
    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "AI Object Detection Service",
        "version": "1.0.0",
        "endpoints": {
            "detect": "/detect/",
            "health": "/health"
        }
    }