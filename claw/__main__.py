#!/usr/bin/env python3

from . import gi_require_version as _

from pathlib import Path
import sys
import re
import threading

import appdirs
from google.oauth2 import service_account
import notify2
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

from .microphone import Microphone
from .google_cloud_speech import Client
from .indicator import Indicator

CREDENTIALS_FILE_NAME = 'credentials.json'
APP_NAME = 'claw'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()
SAMPLE_RATE = 16000
CHUNK_SIZE = SAMPLE_RATE // 10  # 100ms


def display_reponses(responses):
    notification = None

    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
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
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                gtk.main_quit()


def main():
    notify2.init(APP_NAME)

    app_dirs = appdirs.AppDirs(APP_NAME)
    config_dir = Path(app_dirs.user_config_dir)

    credentials_file_path = config_dir.joinpath(CREDENTIALS_FILE_NAME)
    if not credentials_file_path.exists():
        sys.exit("TODO")
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path)

    microphone = Microphone(SAMPLE_RATE, CHUNK_SIZE)
    client = Client(credentials, SAMPLE_RATE)
    Indicator(APP_NAME)

    def listen_to_microphone():
        with microphone as stream:
            responses = client.stream_responses(stream)
            display_reponses(responses)

    thread = threading.Thread(target=listen_to_microphone)
    thread.daemon = True
    thread.start()

    gtk.main()


if __name__ == '__main__':
    main()
