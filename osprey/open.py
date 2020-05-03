import sys
import subprocess

log_file_path = None
history_file_path = None
config_dir_path = None


def open(path):
    if sys.platform == 'darwin':
        subprocess.Popen(['open', path])
    elif sys.platform == 'win32':
        subprocess.Popen(['start', '', path])
    else:
        subprocess.Popen(['xdg-open', path])


def open_log_file():
    global log_file_path
    open(log_file_path)


def open_history_file():
    global history_file_path
    open(history_file_path)


def open_config_dir():
    global config_dir_path
    open(config_dir_path)


def _set_log_file_path(path):
    global log_file_path
    log_file_path = path


def _set_history_file_path(path):
    global history_file_path
    history_file_path = path


def _set_config_dir_path(path):
    global config_dir_path
    config_dir_path = path
