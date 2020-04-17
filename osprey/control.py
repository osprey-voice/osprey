from .app.kaldi import get_singleton

enabled = True


def enable():
    global enabled
    enabled = True


def disable():
    global enabled
    enabled = False


def toggle():
    global enabled
    enabled = not enabled


def is_enabled():
    global enabled
    return enabled


def quit_program():
    get_singleton().engine.disconnect()
