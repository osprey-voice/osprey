import subprocess
import sys

config_dir_path = None
history_file_path = None
log_file_path = None


def open(path):
    if sys.platform == 'darwin':
        subprocess.Popen(['open', path])
    elif sys.platform == 'win32':
        subprocess.Popen(['start', '', path])
    else:
        subprocess.Popen(['xdg-open', path])


def open_config_dir():
    global config_dir_path
    open(config_dir_path)


def open_history_file():
    global history_file_path
    open(history_file_path)


def open_log_file():
    global log_file_path
    open(log_file_path)
