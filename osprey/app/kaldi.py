from dragonfly import get_engine

singleton = None


def get_singleton():
    global singleton
    return singleton


class Kaldi:
    def __init__(self, config_dir):
        self.engine = get_engine(
            'kaldi',

            model_dir=config_dir.joinpath('kaldi_model'),
            tmp_dir=config_dir.joinpath('kaldi_tmp'),

            input_device_index=None,

            retain_dir=None,
            retain_audio=None,
            retain_metadata=None,

            vad_aggressiveness=3,
            vad_padding_start_ms=150,
            vad_padding_end_ms=150,
            vad_complex_padding_end_ms=500,

            auto_add_to_user_lexicon=True,
            lazy_compilation=True,
            invalidate_cache=False,

            alternative_dictation=None,
            cloud_dictation_lang=None,
        )

        global singleton
        singleton = self
