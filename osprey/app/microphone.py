import queue

import pyaudio

singleton = None


def get_singleton():
    global singleton
    return singleton


class Microphone:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, sample_rate, chunk_size, audio_format, audio_channels):
        self._sample_rate = sample_rate
        self._chunk_size = chunk_size
        self._audio_format = audio_format
        self._audio_channels = audio_channels

        self._audio_buffer = queue.Queue()
        self._audio_interface = None
        self._audio_stream = None

        self._open = False

        global singleton
        singleton = self

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=self._audio_format,
            channels=self._audio_channels,
            rate=self._sample_rate,
            input=True,
            frames_per_buffer=self._chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_audio_buffer,
        )

        self._open = True

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._open = False
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._audio_buffer.put(None)
        self._audio_interface.terminate()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._open:
            raise StopIteration
        else:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._audio_buffer.get()
            if chunk is None:
                raise StopIteration
            return chunk

    def _fill_audio_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._audio_buffer.put(in_data)
        return None, pyaudio.paContinue

    def close(self):
        self._open = False
