#!/usr/bin/env python3

from .app import gi_require_version as _

from pathlib import Path
import sys
import re
import threading
import importlib
import itertools

import appdirs
from google.oauth2 import service_account
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify
import evdev
import pyaudio
from google.cloud import speech

from .app.microphone import Microphone
from .app.google_cloud_speech import Client
from .app.indicator import Indicator
from .app.vad import Vad
from .evdev import KEY_MAP
from .voice import context_groups, preferred_phrases
from . import homophones
from . import conversions

APP_NAME = 'osprey'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()

LOG_FILE_NAME = 'logs.txt'
CREDENTIALS_FILE_NAME = 'credentials.json'

SAMPLE_RATE = 16000
CHUNK_SIZE = SAMPLE_RATE // 100  # 10ms
PADDING_DURATION_MS = 2000
VOICED_THRESHOLD = .9
UNVOICED_THRESHOLD = .9
AUDIO_FORMAT = pyaudio.paInt16
# The API currently only supports 1-channel (mono) audio
# https://goo.gl/z757pE
AUDIO_CHANNELS = 1
AUDIO_ENCODING = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16

INTERIM_RESULTS = True
LANGUAGE_CODE = 'en-US'
THRESHOLD_LEVEL = 3


def read_scripts(config_dir):
    for path in config_dir.glob('**/*.py'):
        if path.is_file() and path.stem != '':
            parts = list(path.parts[len(config_dir.parts):-1]) + [path.stem]
            try:
                importlib.import_module('.'.join(parts))
            except Exception as e:
                print(f'Error occurred while loading \'{path}\': {e}', file=sys.stderr)


def compile_regexes():
    for context_group in context_groups.values():
        for context in context_group._contexts.values():
            context._compile()


def display_result(result, notification):
    transcript = result.transcript

    if not result.is_final:
        if notification:
            notification.update(APP_NAME_CAPITALIZED, transcript)
        else:
            notification = Notify.Notification.new(APP_NAME_CAPITALIZED, transcript)
        notification.show()
    else:
        notification.update(f'{APP_NAME_CAPITALIZED} [FINAL]', transcript)
        notification.show()
        notification = None

    return notification


def match_result(result):
    transcript = result.transcript
    for context_group in context_groups.values():
        for context in context_group._contexts.values():
            if context._match(transcript):
                return


def block_until_ready(gen):
    first = next(gen)
    recombined = itertools.chain([first], gen)
    return recombined


def listen_to_microphone(microphone, client, vad):
    notification = None

    with microphone as stream:
        while True:
            # speech = vad.filter_phrases(stream)
            # speech = block_until_ready(speech)
            # results = client.stream_results(speech)
            results = client.stream_results(stream)
            for result in results:
                notification = display_result(result, notification)
                if result.is_final:
                    match_result(result)


def main():
    Notify.init(APP_NAME)

    app_dirs = appdirs.AppDirs(APP_NAME)
    config_dir = Path(app_dirs.user_config_dir)
    log_dir = Path(app_dirs.user_log_dir)
    log_file = log_dir.joinpath(LOG_FILE_NAME)

    credentials_file_path = config_dir.joinpath(CREDENTIALS_FILE_NAME)
    if not credentials_file_path.exists():
        sys.exit("Could not find a credentials file for Google Cloud Speech-to-Text")
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)

    sys.path.append(str(config_dir))
    read_scripts(config_dir)
    compile_regexes()

    microphone = Microphone(SAMPLE_RATE, CHUNK_SIZE, AUDIO_FORMAT, AUDIO_CHANNELS)
    client = Client(credentials, SAMPLE_RATE, AUDIO_ENCODING,
                    preferred_phrases, INTERIM_RESULTS, LANGUAGE_CODE)
    Indicator(APP_NAME, config_dir, log_file)
    vad = Vad(SAMPLE_RATE, CHUNK_SIZE, THRESHOLD_LEVEL,
              PADDING_DURATION_MS, VOICED_THRESHOLD, UNVOICED_THRESHOLD)

    thread = threading.Thread(target=listen_to_microphone, args=(microphone, client, vad))
    thread.daemon = True
    thread.start()

    gtk.main()


if __name__ == '__main__':
    main()
