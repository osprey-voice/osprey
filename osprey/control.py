from . import voice
from .app import kaldi
from .voice import ContextGroup

enabled = True
should_reload_scripts = False


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
    kaldi.singleton.engine.disconnect()


def reload_scripts():
    global should_reload_scripts
    should_reload_scripts = True

    voice.context_groups = {}
    voice.default_context_group = ContextGroup('default')

    kaldi.singleton.engine.disconnect()
