# ai_service/Dockerfile
FROM python:3.9

# Set the working directory
WORKDIR /ai_service
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY ./models ./models
COPY ./aiapp.py .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "aiapp:app", "--host", "0.0.0.0", "--port", "8000"]