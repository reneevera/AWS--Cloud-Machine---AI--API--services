# PictorialTranslator

This AWS Chalice application uploads an image, extracts text using AWS Rekognition, translates the text with AWS Translate, and synthesizes speech using AWS Polly. The API endpoints are in [PictorialTranslator/Capabilities/app.py](PictorialTranslator/Capabilities/app.py) and leverage services found under [PictorialTranslator/Capabilities/chalicelib](PictorialTranslator/Capabilities/chalicelib). User interactions are managed through a web interface in [PictorialTranslator/Website](PictorialTranslator/Website) and tests are available under [PictorialTranslator/testing](PictorialTranslator/testing).

## Features

- Upload images and save them to S3.
- Detect and translate text found in images.
- Synthesize speech for translated text.
- Simple and responsive web interface.

## Getting Started

1. Set up your AWS credentials.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt

3. Deploy the application with Chalice
chalice deploy
