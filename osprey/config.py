config = {
    'enable_by_default': True,
    'enable_ccr': True,
    'enable_notifications': True,
    'kaldi': {
        'vad_aggressiveness': 3,
        'vad_padding_start_ms': 150,
        'vad_padding_end_ms': 150,
        'vad_complex_padding_end_ms': 500,
    },
}


def set_config(custom):
    global config
    config.update(custom)
