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
from .open import _set_config_dir_path, _set_history_file_path, _set_log_file_path

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
            else:
                logging.info(f'Loaded \'{path}\'')


def compile_regexes(grammar):
    for context_group in context_groups.values():
        for context in context_group._contexts.values():
            context._compile(grammar)


def show_notification(transcript):
    Notify.Notification.new(APP_NAME_CAPITALIZED, transcript).show()


def on_recognition(words, rule, node):
    transcript = ' '.join(words)
    if enable_notifications:
        show_notification(transcript)
    history_logger = logging.getLogger('history')
    history_logger.info(f'{rule.name}: \'{transcript}\'')


def signal_handler(sig, frame):
    quit_program()


def main():
    app_dirs = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
    config_dir_path = Path(app_dirs.user_config_dir)
    if sys.platform == 'darwin':
        config_dir_path = Path('~/.config/osprey').expanduser()
    log_file_path = config_dir_path.joinpath(LOG_FILE_NAME)
    history_file_path = config_dir_path.joinpath(HISTORY_FILE_NAME)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file_path, mode='w'),
            logging.StreamHandler()
        ]
    )

    history_logger = logging.getLogger('history')
    history_logger.setLevel(logging.INFO)
    history_handler = logging.FileHandler(history_file_path, mode='w')
    history_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    history_logger.addHandler(history_handler)

    _set_log_file_path(log_file_path)
    _set_history_file_path(history_file_path)
    _set_config_dir_path(config_dir_path)

    sys.path.append(str(config_dir_path))
    read_scripts(config_dir_path)
    config = get_config()

    global enable_notifications
    enable_notifications = config['enable_notifications']

    if not config['enable_by_default']:
        disable()

    Notify.init(APP_NAME)
    Indicator(APP_NAME)
    kaldi = Kaldi(config_dir_path, config['kaldi'])
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


if __name__ == '__main__':
    main()
