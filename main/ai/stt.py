import base64
import tempfile
import os
import requests
from django.conf import settings


def process_audio_and_send_request(base64_audio):
    # Decode base64 audio
    decoded_audio = base64.b64decode(base64_audio)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        temp_audio_file.write(decoded_audio)
        temp_audio_path = temp_audio_file.name

    try:
        # Prepare request parameters
        speech_region = settings.SPEECH_REGION
        speech_key = settings.SPEECH_KEY

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
            # print(response.json())
            message = response.json()["NBest"][0]["Lexical"]
            return message
        else:
            return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

    finally:
        # Clean up the temporary file
        os.unlink(temp_audio_path)