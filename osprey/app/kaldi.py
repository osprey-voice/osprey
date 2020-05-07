from dragonfly import get_engine

singleton = None


class Kaldi:
    def __init__(self, config_dir_path, config):
        self.engine = get_engine(
            'kaldi',

            model_dir=config_dir_path.joinpath('kaldi_model'),
            tmp_dir=config_dir_path.joinpath('kaldi_tmp'),

            input_device_index=None,

            retain_dir=None,
            retain_audio=None,
            retain_metadata=None,

            vad_aggressiveness=config['vad_aggressiveness'],
            vad_padding_start_ms=config['vad_padding_start_ms'],
            vad_padding_end_ms=config['vad_padding_end_ms'],
            vad_complex_padding_end_ms=config['vad_complex_padding_end_ms'],

            auto_add_to_user_lexicon=True,
            lazy_compilation=True,
            invalidate_cache=False,

            alternative_dictation=None,
            cloud_dictation_lang=None,
        )

        global singleton
        singleton = self
