#!/usr/bin/env python3

from pathlib import Path
import sys
import re

import appdirs
from google.oauth2 import service_account
import notify2

from .microphone import Microphone
from .google_cloud_speech import Client
from .applet import Applet

CREDENTIALS_FILE_NAME = 'credentials.json'
APP_NAME = 'claw'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()
SAMPLE_RATE = 16000
CHUNK_SIZE = SAMPLE_RATE // 10  # 100ms


def print_reponses(responses):
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
                break


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

    Applet()

    with microphone as stream:
        responses = client.stream_responses(stream)
        print_reponses(responses)


if __name__ == '__main__':
    main()
