from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
from chalicelib import translation_service
from chalicelib import speech_service

import base64
import json

#####
# chalice app configuration
#####
app = Chalice(app_name='Capabilities')
app.debug = True

#####
# services initialization
#####
storage_location = 'contentcen301345205.aws.ai'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)
translation_service = translation_service.TranslationService()
speech_service = speech_service.SpeechService(storage_service)


#####
# RESTful endpoints
#####
@app.route('/images', methods = ['POST'], cors = True)
def upload_image():
    """processes file upload and saves file to storage service"""
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)

    return image_info


@app.route('/images/{image_id}/headlines', methods = ['POST'], cors = True)
def translate_image_text(image_id):
    """detects then translates text in the specified image as a single line"""
    request_data = json.loads(app.current_request.raw_body)
    from_lang = request_data['fromLang']
    to_lang = request_data['toLang']

    MIN_CONFIDENCE = 80.0

    text_lines = recognition_service.detect_text(image_id)

    # Filter high-confidence lines and join them into one paragraph
    filtered_texts = [line['text'] for line in text_lines if float(line['confidence']) >= MIN_CONFIDENCE]
    if not filtered_texts:
        return []  # No eligible lines

    combined_text = " ".join(filtered_texts)

    # Translate the combined text once
    translated_result = translation_service.translate_text(combined_text, from_lang, to_lang)

    # Return a single element list with the combined text and its translation
    return [{
        'text': combined_text,
        'translation': translated_result,
        'boundingBox': None
    }]


@app.route('/text/synthesize', methods=['POST'], cors=True)
def synthesize_text():
    """synthesizes text to speech"""
    request_data = json.loads(app.current_request.raw_body)
    text = request_data['text']
    language_code = request_data.get('languageCode', 'en-US')
    
    audio_info = speech_service.synthesize_speech(text, language_code)
    return audio_info
