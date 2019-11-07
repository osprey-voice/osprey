import sys
import subprocess


def open(path):
    if sys.platform == 'darwin':
        subprocess.call(['open', path])
    elif sys.platform == 'win32':
        subprocess.call(['start', '', path])
    else:
        subprocess.call(['xdg-open', path])
