from google.cloud import speech

from .engine import EngineResult


class Client:
    def __init__(self, credentials, sample_rate, audio_encoding, preferred_phrases, interim_results, language_code):
        self._credentials = credentials
        self._sample_rate = sample_rate
        self._client = speech.SpeechClient(credentials=credentials)
        self._config = speech.types.RecognitionConfig(
            encoding=audio_encoding,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            speech_contexts=[speech.types.SpeechContext(
                phrases=list(preferred_phrases),
            )],
        )
        self._streaming_config = speech.types.StreamingRecognitionConfig(
            config=self._config,
            interim_results=interim_results,
        )

    def _create_requests(self, stream):
        for content in stream:
            request = speech.types.StreamingRecognizeRequest(audio_content=content)
            yield request

    def _stream_reponses(self, requests):
        return self._client.streaming_recognize(self._streaming_config, requests)

    def _process_responses(self, responses):
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

    def _lowercase_transcript(self, results):
        for result in results:
            yield result._replace(transcript=result.transcript.lower())

    def stream_results(self, stream):
        requests = self._create_requests(stream)
        responses = self._stream_reponses(requests)
        results = self._process_responses(responses)
        results = self._convert_results(results)
        results = self._lowercase_transcript(results)
        return results
