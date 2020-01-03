# https://github.com/wiseman/py-webrtcvad/blob/master/example.py

import collections

import webrtcvad


class VAD:
    """Filters out non-voiced audio frames.

    Given a source of audio frames, yields only
    the voiced audio.

    Uses a padded, sliding window algorithm over the audio frames.
    When more than a threshold of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until a threshold of the frames in
    the window are unvoiced to detrigger.

    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.

    Arguments:

    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    frames - a source of audio frames (sequence or generator).

    Returns: A generator that yields PCM audio data.
    """

    def __init__(self, sample_rate, chunk_size, threshold_level, padding_duration_ms, voiced_threshold, unvoiced_threshold):
        self._sample_rate = sample_rate
        self._frame_duration_ms = chunk_size
        self._voiced_threshold = voiced_threshold
        self._unvoiced_threshold = unvoiced_threshold

        self._webrtcvad = webrtcvad.Vad(threshold_level)
        self._padding_duration_ms = padding_duration_ms
        self._num_padding_frames = self._padding_duration_ms // self._frame_duration_ms

    def filter_phrases(self, frames):
        # We use a deque for our sliding window/ring buffer.
        ring_buffer = collections.deque(maxlen=self._num_padding_frames)
        # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
        # NOTTRIGGERED state.
        triggered = False

        for frame in frames:
            is_speech = self._webrtcvad.is_speech(frame, self._sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                # If we're NOTTRIGGERED and more than a threshold of the frames in
                # the ring buffer are voiced frames, then enter the
                # TRIGGERED state.
                if num_voiced > self._voiced_threshold * ring_buffer.maxlen:
                    triggered = True
                    # We want to yield all the audio we see from now until
                    # we are NOTTRIGGERED, but we have to start with the
                    # audio that's already in the ring buffer.
                    for f, _ in ring_buffer:
                        yield f
                    ring_buffer.clear()
            else:
                # We're in the TRIGGERED state, so collect the audio data
                # and add it to the ring buffer.
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                # If more than a threshold of the frames in the ring buffer are
                # unvoiced, then enter NOTTRIGGERED and return.
                if num_unvoiced > self._unvoiced_threshold * ring_buffer.maxlen:
                    return
