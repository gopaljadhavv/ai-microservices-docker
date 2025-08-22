# AI Object Detection Microservices 🚀

A complete microservice solution for AI-powered object detection using YOLOv8. This project demonstrates a modern, scalable architecture with a beautiful web interface and robust backend processing.

## 🎯 Project Overview

This microservice consists of two main components:
- **UI Service**: Modern web interface for image upload and result visualization
- **AI Service**: Backend service performing object detection using YOLOv8 Nano model

The services communicate seamlessly to provide real-time object detection with bounding boxes and confidence scores.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│   UI Service    │ ──────────────► │   AI Service    │
│   (Port 8002)   │                 │   (Port 8001)   │
│                 │                 │                 │
│ - Modern UI     │                 │ - YOLOv8 Model  │
│ - Drag & Drop   │                 │ - Object Detect │
│ - Real-time     │                 │ - BBox Drawing  │
│ - Responsive    │                 │ - Error Handling│
└─────────────────┘                 └─────────────────┘
```

## ✨ Features

### UI Service
- 🎨 **Modern Interface**: Beautiful, responsive design with gradients and animations
- 📁 **Drag & Drop**: Intuitive file upload experience
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- ⚡ **Real-time Results**: Live display of detection results with statistics
- 🛡️ **Error Handling**: User-friendly error messages and validation
- 📊 **Visual Statistics**: Object count and average confidence display

### AI Service
- 🤖 **YOLOv8 Nano**: Lightweight, fast object detection model
- 🎯 **Bounding Boxes**: Visual overlay on detected objects
- 📈 **Confidence Scores**: Detailed confidence information for each detection
- 🔧 **Error Handling**: Comprehensive error handling and logging
- 🏥 **Health Checks**: Service health monitoring
- ⚡ **CPU Optimized**: No GPU required, runs efficiently on CPU

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **YOLOv8**: State-of-the-art object detection model
- **OpenCV**: Computer vision library for image processing
- **PIL**: Python Imaging Library for image manipulation
- **Docker**: Containerization for easy deployment

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-first approach
- **Modern UI/UX**: Beautiful gradients and animations

## 📁 Directory Structure

```
ai-microservices-docker/
├── docker-compose.yml              # Service orchestration
├── README.md                       # This file
├── DOCUMENTATION.md                # Technical documentation
├── ai_service/                     # AI backend service
│   ├── Dockerfile
│   ├── aiapp.py                   # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   └── models/                    # YOLO model files
│       ├── yolov8n.pt            # PyTorch model
│       └── yolov8n.onnx          # ONNX model
├── ui_service/                    # UI frontend service
│   ├── Dockerfile
│   ├── uiapp.py                  # FastAPI + HTML serving
│   ├── requirements.txt          # Python dependencies
│   └── templates/                # HTML templates
│       └── upload.html           # Main UI interface
└── sample_data/                  # Test images
│    ├── cars_1.png
│    ├── cars.png
│   └── person.png
└── demo_outputs/                  # results
    ├── cars_1_detected.jpg
    ├── cars_1_results.json
    ├── cars_detected.jpg
    ├── cars_results.json
    ├── person_detected.jpg      
    └── person_results.json
```

## 🚀 Quick Start

### Prerequisites
- [Docker](https://www.docker.com/get-started) 🐳
- [Docker Compose](https://docs.docker.com/compose/install/) 📦

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ai-microservices-docker
```

### 2. Build and Run
```bash
docker-compose up --build
```

### 3. Access the Application
- 🌐 **Web Interface**: http://localhost:8002
- 🔧 **AI Service API**: http://localhost:8001
- 📚 **API Documentation**: http://localhost:8001/docs

## 📊 Sample Outputs

Generate sample outputs with bounding boxes and JSON files:

```bash
# Start the services first
docker-compose up --build

# In another terminal, generate samples
python generate_samples.py
```

This will create:
- `demo_outputs/` directory with processed images
- Images with bounding boxes drawn
- JSON files with detection results
- Summary report of all detections

## 🔌 API Endpoints

### AI Service (Port 8001)
- `GET /health` - Service health check
- `POST /detect/` - Object detection endpoint
- `GET /` - Service information
- `GET /docs` - Interactive API documentation

### UI Service (Port 8002)
- `GET /` - Main web interface
- `POST /upload/` - Image upload and detection
- `GET /health` - Service health check
- `GET /api/health` - Comprehensive health check
- `GET /api/info` - Service information

## 📋 Response Format

### Detection Response
```json
{
  "filename": "cars_1.png",
  "objects": [
    {
      "label": "person",
      "x": 100,
      "y": 150,
      "width": 80,
      "height": 200,
      "confidence": 0.95
    }
  ],
  "count": 1,
  "image": "base64_encoded_image_with_boxes"
}
```

## 🧪 Testing

### Sample Images
The project includes test images in `sample_data/`:
- `cars_1.png` - Multiple cars
- `cars.png` - Car detection
- `person.png` - Person detection

### Expected Results
- **cars_1.png**: Multiple car objects with high confidence
- **cars.png**: Car objects with bounding boxes
- **person.png**: Person detection with coordinates

## 🔧 Development

### Manual Setup (Development)
```bash
# AI Service
cd ai_service
pip install -r requirements.txt
python -m uvicorn aiapp:app --host 0.0.0.0 --port 8000

# UI Service (in another terminal)
cd ui_service
pip install -r requirements.txt
python -m uvicorn uiapp:app --host 0.0.0.0 --port 8000
```

### Environment Variables
- `AI_SERVICE_URL`: URL for AI service (default: `http://ai_service:8000/detect`)

## 📈 Performance

### Optimizations
- **Model**: YOLOv8 Nano for faster inference
- **CPU**: Optimized for CPU-only environments
- **Caching**: Model loaded on startup
- **Image Processing**: Efficient bounding box drawing
- **Error Handling**: Graceful degradation

### Limitations
- File size: 5MB maximum
- Formats: JPEG, PNG, GIF
- Processing: Single image at a time

## 🐛 Troubleshooting

### Common Issues

1. **Service Not Starting**
   ```bash
   # Check logs
   docker-compose logs ai_service
   docker-compose logs ui_service
   ```

2. **Model Loading Error**
   - Ensure internet connection for model download
   - Check available RAM (minimum 4GB)

3. **Port Conflicts**
   - Change ports in `docker-compose.yml`
   - Ensure ports 8001 and 8002 are available

### Debug Commands
```bash
# Check service health
curl http://localhost:8001/health
curl http://localhost:8002/health

```

## 📚 Documentation

- **[Technical Documentation](DOCUMENTATION.md)**: Comprehensive implementation details
- **[API Documentation](http://localhost:8001/docs)**: Interactive API docs (when running)
- **Sample Outputs**: Generated examples are saved under `demo_outputs/`

## 🔗 References

### Primary Resources
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenCV Documentation](https://docs.opencv.org/)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Built with ❤️ using FastAPI, YOLOv8, and Docker**
