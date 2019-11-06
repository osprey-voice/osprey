from google.cloud import speech


class Client:
    def __init__(self, credentials, sample_rate):
        self.client = speech.SpeechClient(credentials=credentials)
        self.config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code='en-US')
        self.streaming_config = speech.types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)

    def _convert_requests(self, stream):
        return (speech.types.StreamingRecognizeRequest(audio_content=content) for content in stream)

    def stream_responses(self, stream):
        requests = self._convert_requests(stream)
        return self.client.streaming_recognize(self.streaming_config, requests)
