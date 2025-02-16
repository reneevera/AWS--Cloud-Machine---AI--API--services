import boto3
class SpeechService:
    def __init__(self, storage_service):
        self.client = boto3.client('polly')
        self.storage_service = storage_service

    def synthesize_speech(self, text, language_code='en-US', voice_id='Joanna'):
        response = self.client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode=language_code
        )

        # Generate a unique filename for the audio
        audio_filename = f"speech_{hash(text)}.mp3"
        
        # Upload the audio stream to S3
        if 'AudioStream' in response:
            audio_bytes = response['AudioStream'].read()
            return self.storage_service.upload_file(
                file_bytes=audio_bytes,
                file_name=audio_filename
            )

        return None
