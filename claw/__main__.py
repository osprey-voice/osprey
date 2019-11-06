#!/usr/bin/env python3

from pathlib import Path
import sys

import appdirs
from google.oauth2 import service_account

from .microphone import Microphone
from .google_cloud_speech import Client
from .applet import Applet

CREDENTIALS_FILE_NAME = 'credentials.json'
APPNAME = 'claw'
SAMPLE_RATE = 16000
CHUNK_SIZE = SAMPLE_RATE // 10  # 100ms


def main():
    app_dirs = appdirs.AppDirs(APPNAME)
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
        print(responses)


if __name__ == '__main__':
    main()
