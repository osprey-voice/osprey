from google.cloud import speech

from .engine import EngineResult


CORRECTIONS = {}


class Client:
    def __init__(self, credentials, sample_rate, preferred_phrases):
        self._credentials = credentials
        self._sample_rate = sample_rate
        self._client = speech.SpeechClient(credentials=credentials)
        self._config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code='en-US',
            speech_contexts=[speech.types.SpeechContext(
                phrases=list(preferred_phrases),
            )],
        )
        self._streaming_config = speech.types.StreamingRecognitionConfig(
            config=self._config,
            interim_results=True,
        )

    def _create_requests(self, stream):
        for content in stream:
            request = speech.types.StreamingRecognizeRequest(audio_content=content)
            yield request

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

    def _correct_transcript(self, results):
        for result in results:
            transcript = result.transcript
            for key, val in CORRECTIONS.items():
                transcript = transcript.replace(key, val)
            yield result._replace(transcript=transcript)

    def stream_results(self, stream):
        requests = self._create_requests(stream)
        responses = self._client.streaming_recognize(self._streaming_config, requests)
        results = self._process_responses(responses)
        results = self._convert_results(results)
        results = self._correct_transcript(results)
        return results
