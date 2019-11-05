from google.cloud import speech


LANGUAGE_CODE = 'en-US'
ENCODING = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16


class Client:
    def __init__(self, credentials, sample_rate):
        client = speech.SpeechClient(credentials=credentials)
        config = speech.types.RecognitionConfig(
            encoding=ENCODING,
            sample_rate_hertz=sample_rate,
            language_code=LANGUAGE_CODE)
        streaming_config = speech.types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)
