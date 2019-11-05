#!/usr/bin/env python3

import json
from pathlib import Path
import sys

import appdirs

from .microphone import Microphone
from .google_cloud_speech import Client
from .applet import Applet

CREDENTIALS_FILE_NAME = 'credentials.json'
APPNAME = 'claw'
SAMPLE_RATE = 16000


def main():
    app_dirs = appdirs.AppDirs(APPNAME)
    config_dir = Path(app_dirs.user_config_dir)

    credentials_file_path = config_dir.joinpath(CREDENTIALS_FILE_NAME)
    if not credentials_file_path.exists():
        sys.exit("TODO")
    credentials = json.loads(credentials_file_path.read_text())

    microphone = Microphone(SAMPLE_RATE)

    client = Client(credentials, SAMPLE_RATE)

    Applet()


if __name__ == '__main__':
    main()
