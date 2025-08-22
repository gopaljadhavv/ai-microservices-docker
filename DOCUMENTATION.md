# Technical Documentation

## Overview
This project implements a microservices-based object detection solution composed of:
- UI Service: A FastAPI app serving an HTML UI for uploading images and visualizing results.
- AI Service: A FastAPI app running a lightweight YOLOv8 model for object detection on CPU.

Services communicate over HTTP/JSON. Outputs include images with bounding boxes and corresponding JSON files.

## Architecture
- UI Service (port 8002): Accepts uploads, calls AI, displays and saves results to `demo_outputs/`.
- AI Service (port 8001): Loads YOLOv8n (ONNX) and returns detections with bounding boxes and confidences.
- Orchestration: `docker-compose.yml` builds and runs both containers with healthchecks.

## Tech Choices
- FastAPI for both services (simple, async, great docs UI).
- Ultralytics YOLOv8 Nano (CPU-friendly) via ONNX path for lighter inference requirement.
- OpenCV + PIL for image handling and drawing boxes.
- Docker for reproducibility.

## Endpoints
- AI Service
  - GET `/health`: health.
  - POST `/detect/`: body `{ image: base64, image_path: string }` → returns `{filename, objects: [...], count, image: base64_with_boxes,}`.
- UI Service
  - GET `/`: HTML UI.
  - POST `/upload/`: Multipart image → returns AI response JSON.
  - POST `/save-results/`: Saves JSON and image to `demo_outputs/`.
  - GET `/health`, `/api/health`, `/api/info`.

## How to Run
1) Build and start services
```bash
docker-compose up --build
```
- UI: http://localhost:8002
- AI: http://localhost:8001 (Docs at /docs)

2) Generate sample outputs (optional)
```bash
python generate_samples.py
```
This creates files in `demo_outputs/` for images in `sample_data/`.

## Output Artifacts
- Images with boxes: `<name>_detected.jpg`
- JSON with detections: `<name>_results.json`
- Summary: `summary.json` (when using script)
- Location: `demo_outputs/`

## Implementation Steps
1. Scaffolded FastAPI apps for UI and AI services.
2. Implemented AI `/detect/` to:
   - load ONNX YOLOv8n at startup,
   - decode base64 image, run inference, parse boxes, draw boxes,
   - return base64 image with overlays and structured JSON.
3. Implemented UI `/upload/` to validate file, base64 encode, and call AI.
4. Designed modern, responsive UI (`templates/upload.html`) for drag/drop and visualization.
5. Implemented UI `/save-results/` to persist JSON and image to `demo_outputs/`.
6. Added Dockerfiles for both services and a `docker-compose.yml` with healthchecks.
7. Created `generate_samples.py` to batch process `sample_data/` and write outputs.
8. Wrote documentation and ensured references.

## Notes on CPU Use
- The model is loaded via ONNX and runs on CPU; no GPU is required.
- Dependencies include `onnxruntime` and OpenCV. Torch is present due to Ultralytics dependency set but inference path uses ONNX.

## References

- Ultralytics (YOLOv8): https://github.com/ultralytics/ultralytics
- FastAPI: https://fastapi.tiangolo.com/
- OpenCV: https://opencv.org/

## Troubleshooting
- If healthchecks fail, ensure ports 8001 and 8002 are free and that images built successfully.
- Large images (>5MB) are rejected by UI service.
- If AI errors on model load, verify `ai_service/models/yolov8n.onnx` exists.

## Replication Checklist
- Docker and Docker Compose installed.
- Run `docker-compose up --build` in project root.
- Visit UI at http://localhost:8002, upload an image, save results.
- Optionally run `python generate_samples.py` to populate `demo_outputs/` with examples.


