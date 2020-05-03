#!/usr/bin/env python3

from .app import gi_require_version as _

from pathlib import Path
import sys
import threading
import importlib
import signal
import logging

import appdirs
import dragonfly
from dragonfly import Grammar
from gi.repository import Gtk as gtk, Notify

from .app.indicator import Indicator
from .app.kaldi import Kaldi
from .voice import context_groups, IS_WAYLAND_RUNNING
from .evdev import _open_uinput, _close_uinput
from .control import quit_program, disable
from .config import get_config

APP_NAME = 'osprey'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()
APP_AUTHOR = 'osprey-voice'

LOG_FILE_NAME = 'logs.txt'
HISTORY_FILE_NAME = 'history'

enable_notifications = True


def read_scripts(config_dir):
    for path in config_dir.glob('**/*.py'):
        if path.is_file() and path.stem != '':
            parts = list(path.parts[len(config_dir.parts):-1]) + [path.stem]
            try:
                importlib.import_module('.'.join(parts))
            except Exception as e:
                logging.exception(f'Error occurred while loading \'{path}\': {e}')


def compile_regexes(grammar):
    for context_group in context_groups.values():
        for context in context_group._contexts.values():
            context._compile(grammar)


def show_notification(result):
    Notify.Notification.new(APP_NAME_CAPITALIZED, result).show()


def on_recognition(words, rule, node):
    result = ' '.join(words)
    if enable_notifications:
        show_notification(result)


def signal_handler(sig, frame):
    quit_program()


def redirect_stdout_and_stderr(file):
    sys.stdout = file
    sys.stderr = file


def main():
    app_dirs = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
    config_dir = Path(app_dirs.user_config_dir)
    if sys.platform == 'darwin':
        config_dir = Path('~/.config/osprey').expanduser()
    log_file_path = config_dir.joinpath(LOG_FILE_NAME)
    history_file_path = config_dir.joinpath(HISTORY_FILE_NAME)

    log_file = log_file_path.open('w')
    logging.basicConfig(level=logging.INFO, stream=log_file)
    redirect_stdout_and_stderr(log_file)

    sys.path.append(str(config_dir))
    read_scripts(config_dir)
    config = get_config()

    global enable_notifications
    enable_notifications = config['enable_notifications']

    if not config['enable_by_default']:
        disable()

    Notify.init(APP_NAME)
    Indicator(APP_NAME, config_dir, log_file_path, history_file_path)
    kaldi = Kaldi(config_dir, config['kaldi'])
    kaldi.engine.connect()
    if IS_WAYLAND_RUNNING:
        _open_uinput()
    dragonfly.register_recognition_callback(on_recognition)

    grammar = Grammar('default')
    compile_regexes(grammar)
    grammar.load()

    thread = threading.Thread(target=lambda: gtk.main())
    thread.daemon = True
    thread.start()

    signal.signal(signal.SIGINT, signal_handler)

    kaldi.engine.do_recognition()

    if IS_WAYLAND_RUNNING:
        _close_uinput()
    gtk.main_quit()
    log_file.close()


if __name__ == '__main__':
    main()
