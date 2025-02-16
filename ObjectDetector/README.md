# ObjectDetector

This is an AWS Chalice application for detecting objects in images stored on S3. The backend endpoints are defined in [ObjectDetector/Capabilities/app.py](ObjectDetector/Capabilities/app.py) and utilize services implemented in [ObjectDetector/Capabilities/chalicelib/storage_service.py](ObjectDetector/Capabilities/chalicelib/storage_service.py) and [ObjectDetector/Capabilities/chalicelib/recognition_service.py](ObjectDetector/Capabilities/chalicelib/recognition_service.py). The web front-end is located in the [ObjectDetector/Website](ObjectDetector/Website) directory.

## Features

- Randomly selects an image from S3 and detects objects using AWS Rekognition.
- Provides a simple web interface to display the image and detected object labels with confidence scores.

## Getting Started

1. Configure your AWS credentials.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt

3. Deploy with Chalic
   chalice deploy

4. Run the web interface from the Website folder
   
