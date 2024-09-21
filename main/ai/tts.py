import logging
from django.conf import settings
import uuid
import azure.cognitiveservices.speech as speechsdk


logger = logging.getLogger(__name__)


def speech_to_text(text: str):
    """
    Main method to transform text: str to audio: file
    """

    logger.info(f"Processing STT methods with text {text}")
    
    # path to where save audio file
    file_path = f"{settings.BASE_DIR}/media/audio/{uuid.uuid4()}.wav"
    
    # determine speech config, using credentials
    speech_config = speechsdk.SpeechConfig(subscription=settings.SPEECH_KEY, region=settings.SPEECH_REGION)

    # determine audio config output
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)    

    # determine audio voice by chosen region
    speech_config.speech_synthesis_voice_name='uz-UZ-MadinaNeural'

    # get speech audio, waits until audio is generated
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(text).get()
    
    logger.info(f"Successfuly processed STT methods with text {text}")
    return file_path
