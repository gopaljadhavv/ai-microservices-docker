import base64
import os
import io
from fastapi import FastAPI, HTTPException
from ultralytics import YOLO
from PIL import Image
from pydantic import BaseModel
from typing import List

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

class DetectResponse(BaseModel):
    image: str  # Base64 encoded image with detections
    objects: List[DetectionResult]
    count: int


app = FastAPI(
    title="AI ObjectDetection",
    description="Detecting objects in images using YOLOv8 Nano model."
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Create ONNX model if not exists
onnx_model_path = './ai_service/models/yolov8n.onnx'
if not os.path.exists(onnx_model_path):
    model = YOLO('./ai_service/models/yolov8n.pt')  
    model.export(format='onnx')  

# Load the YOLO ONNX models
onnx_model = YOLO('./ai_service/models/yolov8n.onnx', task="detect")

# POST router for object detection
@app.post("/detect/", response_model=DetectResponse)
async def detect_objects(request: DetectRequest):
    """Handles POST requests to /detect/ endpoint for object detection."""
    encoded_image = request.image

    if not encoded_image:
        raise HTTPException(status_code=400, detail="No image provided.")

    # Decode the Base64 image
    image_data = base64.b64decode(encoded_image)
    img = Image.open(io.BytesIO(image_data))

    # Perform object detection
    result = onnx_model(img, save=True)

    # Process object detection results
    output = []
    for r in result:
        if r.boxes is not None:
            for box, value, prob in zip(r.boxes.xywh, r.boxes.cls, r.boxes.conf):
                detected_label = r.names[value.item()]
                x, y, w, h = box
                confidence = round(prob.item(), 2)
                entry = DetectionResult(
                    label=detected_label,
                    x=int(x),
                    y=int(y),
                    width=int(w),
                    height=int(h),
                    confidence=confidence
                )
                output.append(entry)

    # Encode the image file to Base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the results
    return DetectResponse(
        image=encoded_image,
        objects=output,
        count=len(output)
    )