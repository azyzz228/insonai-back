import logging
import base64
import tempfile
import os
import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def process_audio_and_send_request(base64_audio):
    """
    Main method to transfrom base64 to file, and then use stt module to return text: str
    """
    
    logger.info("Processing TTS methods")
    
    # Decode base64 audio
    decoded_audio = base64.b64decode(base64_audio)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        temp_audio_file.write(decoded_audio)
        temp_audio_path = temp_audio_file.name

    try:
        # Prepare request parameters
        speech_region = settings.SPEECH_REGION_STT
        speech_key = settings.SPEECH_KEY_STT

        url = f"https://{speech_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"

        params = {
            "language": "uz-UZ",
            "format": "detailed"
        }

        headers = {
            "Ocp-Apim-Subscription-Key": speech_key,
            "Content-Type": "audio/wav"
        }

        # Send request
        with open(temp_audio_path, 'rb') as audio_file:
            response = requests.post(url, params=params, headers=headers, data=audio_file)

        # Check response
        if response.status_code == 200:
            
            message = response.json()["NBest"][0]["Lexical"]
            logger.info(f"Successfully processed TTS methods message: {message}")

            return message
        else:
            logger.error("Failed to process TTS methods")
            return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

    finally:
        # Clean up the temporary file
        os.unlink(temp_audio_path)