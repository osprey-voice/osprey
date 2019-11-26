from google.cloud import speech

from .engine import EngineResult


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
        requests = (speech.types.StreamingRecognizeRequest(audio_content=content)
                    for content in stream)
        return requests

    def _filter_invalid_responses(self, responses):
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            yield result

    def _convert_results(self, results):
        for result in results:
            yield EngineResult(result.is_final, result.alternatives[0].transcript.strip())

    def stream_results(self, stream):
        requests = self._convert_requests(stream)
        responses = self._client.streaming_recognize(self._streaming_config, requests)
        results = self._filter_invalid_responses(responses)
        results = self._convert_results(results)
        return results
