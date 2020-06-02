#!/usr/bin/env python3

from .app import gi_require_version as _

import importlib
import logging
import signal
import sys
import threading
from pathlib import Path

import appdirs
import click
import dragonfly
from dragonfly import Grammar
from gi.repository import Gtk as gtk, Notify

from . import config, control, open
from .control import disable, quit_program
from .evdev import _close_uinput, _open_uinput
from .voice import context_groups, IS_WAYLAND_RUNNING
from .app.indicator import Indicator
from .app.kaldi import Kaldi

VERSION = '0.1.0'

APP_AUTHOR = 'osprey-voice'
APP_NAME = 'osprey'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()

HISTORY_FILE_NAME = 'history'
LOG_FILE_NAME = 'logs.txt'

enable_notifications = True


def load_scripts(config_dir_path):
    for path in sorted(config_dir_path.glob('**/*.py')):
        if path.is_file() and path.stem != '':
            parts = list(path.parts[len(config_dir_path.parts):-1]) + [path.stem]
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


def show_notification(message):
    Notify.Notification.new(APP_NAME_CAPITALIZED, message).show()


def on_recognition(words, rule, node):
    transcript = ' '.join(words)
    if enable_notifications:
        show_notification(transcript)
    history_logger = logging.getLogger('history')
    history_logger.info(f'{rule.name}: \'{transcript}\'')


def signal_handler(sig, frame):
    quit_program()


def reload_scripts(config_dir_path):
    load_scripts(config_dir_path)
    grammar = Grammar('default')
    compile_regexes(grammar)
    grammar.load()


@click.command()
@click.version_option(version=VERSION)
def main():
    Notify.init(APP_NAME)
    Indicator(APP_NAME)

    thread = threading.Thread(target=lambda: gtk.main(), daemon=True)
    thread.start()

    app_dirs = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
    if sys.platform == 'darwin':
        config_dir_path = Path('~/.config/osprey').expanduser()
    else:
        config_dir_path = Path(app_dirs.user_config_dir)
    if sys.platform == 'win32':
        log_dir_path = Path(app_dirs.user_log_dir)
    else:
        log_dir_path = Path('~/.local/state/osprey').expanduser()
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir_path.joinpath(LOG_FILE_NAME)
    history_file_path = log_dir_path.joinpath(HISTORY_FILE_NAME)

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

    open.config_dir_path = config_dir_path
    open.history_file_path = history_file_path
    open.log_file_path = log_file_path

    sys.path.append(str(config_dir_path))
    load_scripts(config_dir_path)
    _config = config.config

    global enable_notifications
    enable_notifications = _config['enable_notifications']

    if not _config['enable_by_default']:
        disable()

    kaldi = Kaldi(config_dir_path, _config['kaldi'])
    kaldi.engine.connect()
    if IS_WAYLAND_RUNNING:
        _open_uinput()
    dragonfly.register_recognition_callback(on_recognition)

    grammar = Grammar('default')
    compile_regexes(grammar)
    grammar.load()

    signal.signal(signal.SIGINT, signal_handler)

    kaldi.engine.prepare_for_recognition()
    show_notification('Listening...')
    kaldi.engine.do_recognition()
    while control.should_reload_scripts:
        control.should_reload_scripts = False
        kaldi = Kaldi(config_dir_path, _config['kaldi'])
        kaldi.engine.connect()
        reload_scripts(config_dir_path)
        kaldi.engine.prepare_for_recognition()
        show_notification('Listening...')
        kaldi.engine.do_recognition()

    if IS_WAYLAND_RUNNING:
        _close_uinput()
    gtk.main_quit()


if __name__ == '__main__':
    main()
