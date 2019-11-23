#!/usr/bin/env python3

from .app import gi_require_version as _

from pathlib import Path
import sys
import re
import threading
import importlib

import appdirs
from google.oauth2 import service_account
import notify2
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator
import evdev

from .app.microphone import Microphone
from .app.google_cloud_speech import Client
from .app.indicator import Indicator
from .evdev import KEY_MAP
from .voice import CONTEXT_GROUPS

CREDENTIALS_FILE_NAME = 'credentials.json'
LOG_FILE_NAME = 'logs.txt'
APP_NAME = 'osprey'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()
SAMPLE_RATE = 16000
CHUNK_SIZE = SAMPLE_RATE // 10  # 100ms


def filter_invalid_responses(responses):
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        yield result


def display_results(results):
    notification = None

    for result in results:
        transcript = result.alternatives[0].transcript.strip()

        if not result.is_final:
            if notification:
                notification.update(APP_NAME_CAPITALIZED, transcript)
            else:
                notification = notify2.Notification(APP_NAME_CAPITALIZED, transcript)
            notification.show()
        else:
            notification.update(APP_NAME_CAPITALIZED, transcript)
            notification.show()
            notification = None

        yield result


def filter_final_results(results):
    for result in results:
        if result.is_final:
            yield result


def main():
    notify2.init(APP_NAME)

    app_dirs = appdirs.AppDirs(APP_NAME)
    config_dir = Path(app_dirs.user_config_dir)
    log_dir = Path(app_dirs.user_log_dir)
    log_file = log_dir.joinpath(LOG_FILE_NAME)

    credentials_file_path = config_dir.joinpath(CREDENTIALS_FILE_NAME)
    if not credentials_file_path.exists():
        sys.exit("TODO")
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)

    microphone = Microphone(SAMPLE_RATE, CHUNK_SIZE)
    client = Client(credentials, SAMPLE_RATE)
    Indicator(APP_NAME, config_dir, log_file)

    # read scripts
    sys.path.append(str(config_dir))
    for file in config_dir.iterdir():
        if file.is_file() and file.suffix == '.py':
            importlib.import_module(file.stem)

    # compile regexes
    for context_group in CONTEXT_GROUPS:
        for context in context_group._contexts:
            context._compile()

    def listen_to_microphone():
        with microphone as stream:
            responses = client.stream_responses(stream)
            results = filter_invalid_responses(responses)
            results = display_results(results)
            final_results = filter_final_results(results)
            for result in final_results:
                transcript = result.alternatives[0].transcript.strip()

                def search():
                    for context_group in CONTEXT_GROUPS:
                        for context in context_group._contexts:
                            if context._match(transcript):
                                return
                search()

    thread = threading.Thread(target=listen_to_microphone)
    thread.daemon = True
    thread.start()

    gtk.main()


if __name__ == '__main__':
    main()
