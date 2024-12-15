# ui_service/Dockerfile
FROM python:3.9

# Set the working directory
WORKDIR /ui_service

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY ./templates ./templates
COPY ./uiapp.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "uiapp:app", "--host", "0.0.0.0", "--port", "8000"]