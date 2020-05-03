import sys
import subprocess


def open(path):
    if sys.platform == 'darwin':
        subprocess.Popen(['open', path])
    elif sys.platform == 'win32':
        subprocess.Popen(['start', '', path])
    else:
        subprocess.Popen(['xdg-open', path])
