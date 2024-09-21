from django.conf import settings
import uuid
import azure.cognitiveservices.speech as speechsdk

def speech_to_text(text: str):
    file_path = f"{settings.BASE_DIR}/media/audio/{uuid.uuid4()}.wav"
    speech_config = speechsdk.SpeechConfig(subscription=settings.SPEECH_KEY, region=settings.SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)    

    speech_config.speech_synthesis_voice_name='uz-UZ-MadinaNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(text).get()
    return file_path
