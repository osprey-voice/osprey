from google.cloud import speech


class Client:
    def __init__(self, credentials, sample_rate):
        self._credentials = credentials
        self._sample_rate = sample_rate
        self._client = speech.SpeechClient(credentials=credentials)
        self._config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code='en-US')
        self._streaming_config = speech.types.StreamingRecognitionConfig(
            config=self._config,
            interim_results=True)

    def _convert_requests(self, stream):
        return (speech.types.StreamingRecognizeRequest(audio_content=content) for content in stream)

    def stream_responses(self, stream):
        requests = self._convert_requests(stream)
        return self._client.streaming_recognize(self._streaming_config, requests)
