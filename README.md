# AI-UI Backend Microservices Project 🚀
This project consists of two microservices: `ui_service` and `ai_service`. The `ui_service` acts as the basic frontend, while the `ai_service` handles backend processing where inference of images takes place in real time using ONNX.


## Directory Structure 📁

```
project-root/
├── docker-compose.yml
├── README.md
├── ai_service/
│   ├── Dockerfile
│   ├── aiapp.py
│   ├── requirements.txt
│   └── models/
│       ├── yolov8n.onnx
│       └── yolov8n.pt
│   
└── ui_service/
    ├── uiapp.py
    ├── Dockerfile
    ├── requirements.txt
    └── templates/
        └── upload.html
```

## Prerequisites ⚙️

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) 🐳
- [Docker Compose](https://docs.docker.com/compose/install/) 📦

## Getting Started 🚀

1. **Clone the Repository**: If you haven't already, clone the repository to your local machine.

   ```bash
   git clone https://github.com/gopaljadhavv/ai-microservices-docker.git
   cd ai-microservices-docker
   ```

2. **Build and Run the Services**: Use Docker Compose to build and run the services.

   ```bash
   docker-compose up
   ```

3. **Access the Services**:
   - The `ui_service` will be available at `http://localhost:8002` 🌐
   - The `ai_service` will be available at `http://localhost:8001` 🌐

## Service Details 🛠️

### ui_service

- **Build Context**: `./ui_service`
- **Port**: Exposed on `8002`
- **Environment Variables**:
  - `AI_SERVICE_URL`: URL for the AI service (default: `http://ai_service:8000/detect`)
- **Health Check**: Checks the health of the service every 30 seconds.

### ai_service

- **Build Context**: `./ai_service`
- **Port**: Exposed on `8001`
- **Health Check**: Checks the health of the service every 30 seconds.

## Output 📊

When you run this project and access the UI service, you'll be able to:

1. Upload an image through the web interface.
2. The image will be sent to the AI service for processing.
3. The AI service will perform object detection using the YOLO model.
4. The results will be sent back to the UI service.
5. Returns a JSON response containing:
    - **Image**: Base64 encoded image with detections.
    - **Objects**: List of detected objects with their properties.
    - **Count**: Number of detected objects.

The output provides real-time object detection capabilities, allowing you to identify and locate various objects within the images.

## Notes 📝

- Ensure that the directory structure is maintained as shown above.
- If you encounter any issues, make sure Docker and Docker Compose are properly installed and running.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Tags 🏷️

- **Docker** 🐳
- **Microservices** 🌐
- **FastAPI** ⚡
- **ONNX** 📊
- **YOLO** 🤖
- **Image Processing** 🖼️
- **Object Detection** 🔍
- **Python** 🐍
- **Machine Learning** 🤖
- **Computer Vision** 👁️
