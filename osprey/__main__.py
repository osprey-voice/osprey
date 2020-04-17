#!/usr/bin/env python3

from .app import gi_require_version as _

from pathlib import Path
import sys
import threading
import importlib
import signal

import appdirs
from dragonfly import Grammar
from gi.repository import Gtk as gtk, Notify

from .app.indicator import Indicator
from .app.kaldi import Kaldi
from .voice import context_groups, _open_uinput, _close_uinput
from .control import quit_program

APP_NAME = 'osprey'
APP_NAME_CAPITALIZED = APP_NAME.capitalize()

LOG_FILE_NAME = 'logs.txt'


def read_scripts(config_dir):
    for path in config_dir.glob('**/*.py'):
        if path.is_file() and path.stem != '':
            parts = list(path.parts[len(config_dir.parts):-1]) + [path.stem]
            try:
                importlib.import_module('.'.join(parts))
            except Exception as e:
                print(f'Error occurred while loading \'{path}\': {e}', file=sys.stderr)


def compile_regexes(grammar):
    for context_group in context_groups.values():
        for context in context_group._contexts.values():
            context._compile(grammar)


def display_result(result, notification):
    transcript = result.transcript

    title = APP_NAME_CAPITALIZED
    if result.is_final:
        title += ' [FINAL]'

    if notification:
        notification.update(title, transcript)
    else:
        notification = Notify.Notification.new(title, transcript)

    notification.show()

    if result.is_final:
        notification = None

    return notification


def signal_handler(sig, frame):
    quit_program()


def main():
    app_dirs = appdirs.AppDirs(APP_NAME)
    config_dir = Path(app_dirs.user_config_dir)
    log_dir = Path(app_dirs.user_log_dir)
    log_file = log_dir.joinpath(LOG_FILE_NAME)

    Notify.init(APP_NAME)
    Indicator(APP_NAME, config_dir, log_file)
    kaldi = Kaldi(config_dir)
    kaldi.engine.connect()
    _open_uinput()

    grammar = Grammar('default')
    sys.path.append(str(config_dir))
    read_scripts(config_dir)
    compile_regexes(grammar)
    grammar.load()

    thread = threading.Thread(target=lambda: gtk.main())
    thread.daemon = True
    thread.start()

    signal.signal(signal.SIGINT, signal_handler)

    # notification = None
    kaldi.engine.do_recognition()

    _close_uinput()
    gtk.main_quit()


if __name__ == '__main__':
    main()
