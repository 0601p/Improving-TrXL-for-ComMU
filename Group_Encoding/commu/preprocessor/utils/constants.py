import enum
from typing import List, Optional

class KeySwitchVelocity(int, enum.Enum):
    DEFAULT = 1

    @classmethod
    def get_value(cls, key: Optional[str]) -> int:
        key = key or "DEFAULT"
        if hasattr(cls, key):
            return getattr(cls, key).value
        return cls.DEFAULT.value

class ChordType(str, enum.Enum):
    MAJOR = "major"
    MINOR = "minor"

    @classmethod
    def values(cls) -> List[str]:
        return list(cls.__members__.values())

BPM_INTERVAL = 5
CHORD_TRACK_NAME = "chord"
DEFAULT_NUM_BEATS = 4
DEFAULT_POSITION_RESOLUTION = 128
DEFAULT_TICKS_PER_BEAT = 480
MAX_BPM = 200
NUM_BPM_AUGMENT = 2
NUM_KEY_AUGMENT = 6
UNKNOWN = "unknown"
VELOCITY_INTERVAL = 2

MAJOR_KEY = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
MINOR_KEY = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

KEY_MAP = {
    "cmajor": 0,
    "c#major": 1,
    "dbmajor": 1,
    "dmajor": 2,
    "d#major": 3,
    "ebmajor": 3,
    "emajor": 4,
    "fmajor": 5,
    "f#major": 6,
    "gbmajor": 6,
    "gmajor": 7,
    "g#major": 8,
    "abmajor": 8,
    "amajor": 9,
    "a#major": 10,
    "bbmajor": 10,
    "bmajor": 11,
    "cminor": 12,
    "c#minor": 13,
    "dbminor": 13,
    "dminor": 14,
    "d#minor": 15,
    "ebminor": 15,
    "eminor": 16,
    "fminor": 17,
    "f#minor": 18,
    "gbminor": 18,
    "gminor": 19,
    "g#minor": 20,
    "abminor": 20,
    "aminor": 21,
    "a#minor": 22,
    "bbminor": 22,
    "bminor": 23,
}

KEY_NUM_MAP = {v: k for k, v in KEY_MAP.items()}

TIME_SIG_MAP = {
    "4/4": 0,
    "3/4": 1,
    "6/8": 2,
    "12/8": 3,
}

SIG_TIME_MAP = {v: k for k, v in TIME_SIG_MAP.items()}

PITCH_RANGE_MAP = {
    "very_low": 0,
    "low": 1,
    "mid_low": 2,
    "mid": 3,
    "mid_high": 4,
    "high": 5,
    "very_high": 6,
}

INST_MAP = {'accordion': 1,
 'acoustic_bass': 3,
 'acoustic_guitar': 3,
 'acoustic_piano': 0,
 'banjo': 3,
 'bassoon': 5,
 'bell': 2,
 'brass_ensemble': 5,
 'celesta': 2,
 'choir': 7,
 'clarinet': 5,
 'drums_full': 6,
 'drums_tops': 6,
 'electric_bass': 3,
 'electric_guitar_clean': 3,
 'electric_guitar_distortion': 3,
 'electric_piano': 0,
 'fiddle': 4,
 'flute': 5,
 'glockenspiel': 2,
 'harp': 3,
 'harpsichord': 0,
 'horn': 5,
 'keyboard': 0,
 'mandolin': 3,
 'marimba': 2,
 'nylon_guitar': 3,
 'oboe': 5,
 'organ': 0,
 'oud': 3,
 'pad_synth': 4,
 'percussion': 6,
 'recorder': 5,
 'sitar': 3,
 'string_cello': 4,
 'string_double_bass': 4,
 'string_ensemble': 4,
 'string_viola': 4,
 'string_violin': 4,
 'synth_bass': 3,
 'synth_bass_808': 3,
 'synth_bass_wobble': 3,
 'synth_bell': 2,
 'synth_lead': 1,
 'synth_pad': 4,
 'synth_pluck': 7,
 'synth_voice': 7,
 'timpani': 6,
 'trombone': 5,
 'trumpet': 5,
 'tuba': 5,
 'ukulele': 3,
 'vibraphone': 2,
 'whistle': 7,
 'xylophone': 2,
 'zither': 3,
 'orgel': 2,
 'synth_brass': 5,
 'sax': 5,
 'bamboo_flute': 5,
 'yanggeum': 3,
 'vocal': 8,
 'accordion-1': 1,
 'accordion-2': 1,
 'accordion-3': 1,
 'accordion-4': 1,
 'accordion-5': 1,
 'accordion-6': 1,
 'accordion-7': 1,
 'accordion-8': 1,
 'accordion-9': 1,
 'accordion-10': 1,
 'accordion-11': 1,
 'accordion-12': 1,
 'accordion-13': 1,
 'accordion-14': 1,
 'accordion-15': 1,
 'acoustic_bass-1': 3,
 'acoustic_bass-2': 3,
 'acoustic_bass-3': 3,
 'acoustic_bass-4': 3,
 'acoustic_bass-5': 3,
 'acoustic_bass-6': 3,
 'acoustic_bass-7': 3,
 'acoustic_bass-8': 3,
 'acoustic_bass-9': 3,
 'acoustic_bass-10': 3,
 'acoustic_bass-11': 3,
 'acoustic_bass-12': 3,
 'acoustic_bass-13': 3,
 'acoustic_bass-14': 3,
 'acoustic_bass-15': 3,
 'acoustic_guitar-1': 3,
 'acoustic_guitar-2': 3,
 'acoustic_guitar-3': 3,
 'acoustic_guitar-4': 3,
 'acoustic_guitar-5': 3,
 'acoustic_guitar-6': 3,
 'acoustic_guitar-7': 3,
 'acoustic_guitar-8': 3,
 'acoustic_guitar-9': 3,
 'acoustic_guitar-10': 3,
 'acoustic_guitar-11': 3,
 'acoustic_guitar-12': 3,
 'acoustic_guitar-13': 3,
 'acoustic_guitar-14': 3,
 'acoustic_guitar-15': 3,
 'acoustic_piano-1': 0,
 'acoustic_piano-2': 0,
 'acoustic_piano-3': 0,
 'acoustic_piano-4': 0,
 'acoustic_piano-5': 0,
 'acoustic_piano-6': 0,
 'acoustic_piano-7': 0,
 'acoustic_piano-8': 0,
 'acoustic_piano-9': 0,
 'acoustic_piano-10': 0,
 'acoustic_piano-11': 0,
 'acoustic_piano-12': 0,
 'acoustic_piano-13': 0,
 'acoustic_piano-14': 0,
 'acoustic_piano-15': 0,
 'banjo-1': 3,
 'banjo-2': 3,
 'banjo-3': 3,
 'banjo-4': 3,
 'banjo-5': 3,
 'banjo-6': 3,
 'banjo-7': 3,
 'banjo-8': 3,
 'banjo-9': 3,
 'banjo-10': 3,
 'banjo-11': 3,
 'banjo-12': 3,
 'banjo-13': 3,
 'banjo-14': 3,
 'banjo-15': 3,
 'bassoon-1': 5,
 'bassoon-2': 5,
 'bassoon-3': 5,
 'bassoon-4': 5,
 'bassoon-5': 5,
 'bassoon-6': 5,
 'bassoon-7': 5,
 'bassoon-8': 5,
 'bassoon-9': 5,
 'bassoon-10': 5,
 'bassoon-11': 5,
 'bassoon-12': 5,
 'bassoon-13': 5,
 'bassoon-14': 5,
 'bassoon-15': 5,
 'bell-1': 2,
 'bell-2': 2,
 'bell-3': 2,
 'bell-4': 2,
 'bell-5': 2,
 'bell-6': 2,
 'bell-7': 2,
 'bell-8': 2,
 'bell-9': 2,
 'bell-10': 2,
 'bell-11': 2,
 'bell-12': 2,
 'bell-13': 2,
 'bell-14': 2,
 'bell-15': 2,
 'brass_ensemble-1': 5,
 'brass_ensemble-2': 5,
 'brass_ensemble-3': 5,
 'brass_ensemble-4': 5,
 'brass_ensemble-5': 5,
 'brass_ensemble-6': 5,
 'brass_ensemble-7': 5,
 'brass_ensemble-8': 5,
 'brass_ensemble-9': 5,
 'brass_ensemble-10': 5,
 'brass_ensemble-11': 5,
 'brass_ensemble-12': 5,
 'brass_ensemble-13': 5,
 'brass_ensemble-14': 5,
 'brass_ensemble-15': 5,
 'celesta-1': 2,
 'celesta-2': 2,
 'celesta-3': 2,
 'celesta-4': 2,
 'celesta-5': 2,
 'celesta-6': 2,
 'celesta-7': 2,
 'celesta-8': 2,
 'celesta-9': 2,
 'celesta-10': 2,
 'celesta-11': 2,
 'celesta-12': 2,
 'celesta-13': 2,
 'celesta-14': 2,
 'celesta-15': 2,
 'choir-1': 7,
 'choir-2': 7,
 'choir-3': 7,
 'choir-4': 7,
 'choir-5': 7,
 'choir-6': 7,
 'choir-7': 7,
 'choir-8': 7,
 'choir-9': 7,
 'choir-10': 7,
 'choir-11': 7,
 'choir-12': 7,
 'choir-13': 7,
 'choir-14': 7,
 'choir-15': 7,
 'clarinet-1': 5,
 'clarinet-2': 5,
 'clarinet-3': 5,
 'clarinet-4': 5,
 'clarinet-5': 5,
 'clarinet-6': 5,
 'clarinet-7': 5,
 'clarinet-8': 5,
 'clarinet-9': 5,
 'clarinet-10': 5,
 'clarinet-11': 5,
 'clarinet-12': 5,
 'clarinet-13': 5,
 'clarinet-14': 5,
 'clarinet-15': 5,
 'drums_full-1': 6,
 'drums_full-2': 6,
 'drums_full-3': 6,
 'drums_full-4': 6,
 'drums_full-5': 6,
 'drums_full-6': 6,
 'drums_full-7': 6,
 'drums_full-8': 6,
 'drums_full-9': 6,
 'drums_full-10': 6,
 'drums_full-11': 6,
 'drums_full-12': 6,
 'drums_full-13': 6,
 'drums_full-14': 6,
 'drums_full-15': 6,
 'drums_tops-1': 6,
 'drums_tops-2': 6,
 'drums_tops-3': 6,
 'drums_tops-4': 6,
 'drums_tops-5': 6,
 'drums_tops-6': 6,
 'drums_tops-7': 6,
 'drums_tops-8': 6,
 'drums_tops-9': 6,
 'drums_tops-10': 6,
 'drums_tops-11': 6,
 'drums_tops-12': 6,
 'drums_tops-13': 6,
 'drums_tops-14': 6,
 'drums_tops-15': 6,
 'electric_bass-1': 3,
 'electric_bass-2': 3,
 'electric_bass-3': 3,
 'electric_bass-4': 3,
 'electric_bass-5': 3,
 'electric_bass-6': 3,
 'electric_bass-7': 3,
 'electric_bass-8': 3,
 'electric_bass-9': 3,
 'electric_bass-10': 3,
 'electric_bass-11': 3,
 'electric_bass-12': 3,
 'electric_bass-13': 3,
 'electric_bass-14': 3,
 'electric_bass-15': 3,
 'electric_guitar_clean-1': 3,
 'electric_guitar_clean-2': 3,
 'electric_guitar_clean-3': 3,
 'electric_guitar_clean-4': 3,
 'electric_guitar_clean-5': 3,
 'electric_guitar_clean-6': 3,
 'electric_guitar_clean-7': 3,
 'electric_guitar_clean-8': 3,
 'electric_guitar_clean-9': 3,
 'electric_guitar_clean-10': 3,
 'electric_guitar_clean-11': 3,
 'electric_guitar_clean-12': 3,
 'electric_guitar_clean-13': 3,
 'electric_guitar_clean-14': 3,
 'electric_guitar_clean-15': 3,
 'electric_guitar_distortion-1': 3,
 'electric_guitar_distortion-2': 3,
 'electric_guitar_distortion-3': 3,
 'electric_guitar_distortion-4': 3,
 'electric_guitar_distortion-5': 3,
 'electric_guitar_distortion-6': 3,
 'electric_guitar_distortion-7': 3,
 'electric_guitar_distortion-8': 3,
 'electric_guitar_distortion-9': 3,
 'electric_guitar_distortion-10': 3,
 'electric_guitar_distortion-11': 3,
 'electric_guitar_distortion-12': 3,
 'electric_guitar_distortion-13': 3,
 'electric_guitar_distortion-14': 3,
 'electric_guitar_distortion-15': 3,
 'electric_piano-1': 0,
 'electric_piano-2': 0,
 'electric_piano-3': 0,
 'electric_piano-4': 0,
 'electric_piano-5': 0,
 'electric_piano-6': 0,
 'electric_piano-7': 0,
 'electric_piano-8': 0,
 'electric_piano-9': 0,
 'electric_piano-10': 0,
 'electric_piano-11': 0,
 'electric_piano-12': 0,
 'electric_piano-13': 0,
 'electric_piano-14': 0,
 'electric_piano-15': 0,
 'fiddle-1': 4,
 'fiddle-2': 4,
 'fiddle-3': 4,
 'fiddle-4': 4,
 'fiddle-5': 4,
 'fiddle-6': 4,
 'fiddle-7': 4,
 'fiddle-8': 4,
 'fiddle-9': 4,
 'fiddle-10': 4,
 'fiddle-11': 4,
 'fiddle-12': 4,
 'fiddle-13': 4,
 'fiddle-14': 4,
 'fiddle-15': 4,
 'flute-1': 5,
 'flute-2': 5,
 'flute-3': 5,
 'flute-4': 5,
 'flute-5': 5,
 'flute-6': 5,
 'flute-7': 5,
 'flute-8': 5,
 'flute-9': 5,
 'flute-10': 5,
 'flute-11': 5,
 'flute-12': 5,
 'flute-13': 5,
 'flute-14': 5,
 'flute-15': 5,
 'glockenspiel-1': 2,
 'glockenspiel-2': 2,
 'glockenspiel-3': 2,
 'glockenspiel-4': 2,
 'glockenspiel-5': 2,
 'glockenspiel-6': 2,
 'glockenspiel-7': 2,
 'glockenspiel-8': 2,
 'glockenspiel-9': 2,
 'glockenspiel-10': 2,
 'glockenspiel-11': 2,
 'glockenspiel-12': 2,
 'glockenspiel-13': 2,
 'glockenspiel-14': 2,
 'glockenspiel-15': 2,
 'harp-1': 3,
 'harp-2': 3,
 'harp-3': 3,
 'harp-4': 3,
 'harp-5': 3,
 'harp-6': 3,
 'harp-7': 3,
 'harp-8': 3,
 'harp-9': 3,
 'harp-10': 3,
 'harp-11': 3,
 'harp-12': 3,
 'harp-13': 3,
 'harp-14': 3,
 'harp-15': 3,
 'harpsichord-1': 0,
 'harpsichord-2': 0,
 'harpsichord-3': 0,
 'harpsichord-4': 0,
 'harpsichord-5': 0,
 'harpsichord-6': 0,
 'harpsichord-7': 0,
 'harpsichord-8': 0,
 'harpsichord-9': 0,
 'harpsichord-10': 0,
 'harpsichord-11': 0,
 'harpsichord-12': 0,
 'harpsichord-13': 0,
 'harpsichord-14': 0,
 'harpsichord-15': 0,
 'horn-1': 5,
 'horn-2': 5,
 'horn-3': 5,
 'horn-4': 5,
 'horn-5': 5,
 'horn-6': 5,
 'horn-7': 5,
 'horn-8': 5,
 'horn-9': 5,
 'horn-10': 5,
 'horn-11': 5,
 'horn-12': 5,
 'horn-13': 5,
 'horn-14': 5,
 'horn-15': 5,
 'keyboard-1': 0,
 'keyboard-2': 0,
 'keyboard-3': 0,
 'keyboard-4': 0,
 'keyboard-5': 0,
 'keyboard-6': 0,
 'keyboard-7': 0,
 'keyboard-8': 0,
 'keyboard-9': 0,
 'keyboard-10': 0,
 'keyboard-11': 0,
 'keyboard-12': 0,
 'keyboard-13': 0,
 'keyboard-14': 0,
 'keyboard-15': 0,
 'mandolin-1': 3,
 'mandolin-2': 3,
 'mandolin-3': 3,
 'mandolin-4': 3,
 'mandolin-5': 3,
 'mandolin-6': 3,
 'mandolin-7': 3,
 'mandolin-8': 3,
 'mandolin-9': 3,
 'mandolin-10': 3,
 'mandolin-11': 3,
 'mandolin-12': 3,
 'mandolin-13': 3,
 'mandolin-14': 3,
 'mandolin-15': 3,
 'marimba-1': 2,
 'marimba-2': 2,
 'marimba-3': 2,
 'marimba-4': 2,
 'marimba-5': 2,
 'marimba-6': 2,
 'marimba-7': 2,
 'marimba-8': 2,
 'marimba-9': 2,
 'marimba-10': 2,
 'marimba-11': 2,
 'marimba-12': 2,
 'marimba-13': 2,
 'marimba-14': 2,
 'marimba-15': 2,
 'nylon_guitar-1': 3,
 'nylon_guitar-2': 3,
 'nylon_guitar-3': 3,
 'nylon_guitar-4': 3,
 'nylon_guitar-5': 3,
 'nylon_guitar-6': 3,
 'nylon_guitar-7': 3,
 'nylon_guitar-8': 3,
 'nylon_guitar-9': 3,
 'nylon_guitar-10': 3,
 'nylon_guitar-11': 3,
 'nylon_guitar-12': 3,
 'nylon_guitar-13': 3,
 'nylon_guitar-14': 3,
 'nylon_guitar-15': 3,
 'oboe-1': 5,
 'oboe-2': 5,
 'oboe-3': 5,
 'oboe-4': 5,
 'oboe-5': 5,
 'oboe-6': 5,
 'oboe-7': 5,
 'oboe-8': 5,
 'oboe-9': 5,
 'oboe-10': 5,
 'oboe-11': 5,
 'oboe-12': 5,
 'oboe-13': 5,
 'oboe-14': 5,
 'oboe-15': 5,
 'organ-1': 0,
 'organ-2': 0,
 'organ-3': 0,
 'organ-4': 0,
 'organ-5': 0,
 'organ-6': 0,
 'organ-7': 0,
 'organ-8': 0,
 'organ-9': 0,
 'organ-10': 0,
 'organ-11': 0,
 'organ-12': 0,
 'organ-13': 0,
 'organ-14': 0,
 'organ-15': 0,
 'oud-1': 3,
 'oud-2': 3,
 'oud-3': 3,
 'oud-4': 3,
 'oud-5': 3,
 'oud-6': 3,
 'oud-7': 3,
 'oud-8': 3,
 'oud-9': 3,
 'oud-10': 3,
 'oud-11': 3,
 'oud-12': 3,
 'oud-13': 3,
 'oud-14': 3,
 'oud-15': 3,
 'pad_synth-1': 4,
 'pad_synth-2': 4,
 'pad_synth-3': 4,
 'pad_synth-4': 4,
 'pad_synth-5': 4,
 'pad_synth-6': 4,
 'pad_synth-7': 4,
 'pad_synth-8': 4,
 'pad_synth-9': 4,
 'pad_synth-10': 4,
 'pad_synth-11': 4,
 'pad_synth-12': 4,
 'pad_synth-13': 4,
 'pad_synth-14': 4,
 'pad_synth-15': 4,
 'percussion-1': 6,
 'percussion-2': 6,
 'percussion-3': 6,
 'percussion-4': 6,
 'percussion-5': 6,
 'percussion-6': 6,
 'percussion-7': 6,
 'percussion-8': 6,
 'percussion-9': 6,
 'percussion-10': 6,
 'percussion-11': 6,
 'percussion-12': 6,
 'percussion-13': 6,
 'percussion-14': 6,
 'percussion-15': 6,
 'recorder-1': 5,
 'recorder-2': 5,
 'recorder-3': 5,
 'recorder-4': 5,
 'recorder-5': 5,
 'recorder-6': 5,
 'recorder-7': 5,
 'recorder-8': 5,
 'recorder-9': 5,
 'recorder-10': 5,
 'recorder-11': 5,
 'recorder-12': 5,
 'recorder-13': 5,
 'recorder-14': 5,
 'recorder-15': 5,
 'sitar-1': 3,
 'sitar-2': 3,
 'sitar-3': 3,
 'sitar-4': 3,
 'sitar-5': 3,
 'sitar-6': 3,
 'sitar-7': 3,
 'sitar-8': 3,
 'sitar-9': 3,
 'sitar-10': 3,
 'sitar-11': 3,
 'sitar-12': 3,
 'sitar-13': 3,
 'sitar-14': 3,
 'sitar-15': 3,
 'string_cello-1': 4,
 'string_cello-2': 4,
 'string_cello-3': 4,
 'string_cello-4': 4,
 'string_cello-5': 4,
 'string_cello-6': 4,
 'string_cello-7': 4,
 'string_cello-8': 4,
 'string_cello-9': 4,
 'string_cello-10': 4,
 'string_cello-11': 4,
 'string_cello-12': 4,
 'string_cello-13': 4,
 'string_cello-14': 4,
 'string_cello-15': 4,
 'string_double_bass-1': 4,
 'string_double_bass-2': 4,
 'string_double_bass-3': 4,
 'string_double_bass-4': 4,
 'string_double_bass-5': 4,
 'string_double_bass-6': 4,
 'string_double_bass-7': 4,
 'string_double_bass-8': 4,
 'string_double_bass-9': 4,
 'string_double_bass-10': 4,
 'string_double_bass-11': 4,
 'string_double_bass-12': 4,
 'string_double_bass-13': 4,
 'string_double_bass-14': 4,
 'string_double_bass-15': 4,
 'string_ensemble-1': 4,
 'string_ensemble-2': 4,
 'string_ensemble-3': 4,
 'string_ensemble-4': 4,
 'string_ensemble-5': 4,
 'string_ensemble-6': 4,
 'string_ensemble-7': 4,
 'string_ensemble-8': 4,
 'string_ensemble-9': 4,
 'string_ensemble-10': 4,
 'string_ensemble-11': 4,
 'string_ensemble-12': 4,
 'string_ensemble-13': 4,
 'string_ensemble-14': 4,
 'string_ensemble-15': 4,
 'string_viola-1': 4,
 'string_viola-2': 4,
 'string_viola-3': 4,
 'string_viola-4': 4,
 'string_viola-5': 4,
 'string_viola-6': 4,
 'string_viola-7': 4,
 'string_viola-8': 4,
 'string_viola-9': 4,
 'string_viola-10': 4,
 'string_viola-11': 4,
 'string_viola-12': 4,
 'string_viola-13': 4,
 'string_viola-14': 4,
 'string_viola-15': 4,
 'string_violin-1': 4,
 'string_violin-2': 4,
 'string_violin-3': 4,
 'string_violin-4': 4,
 'string_violin-5': 4,
 'string_violin-6': 4,
 'string_violin-7': 4,
 'string_violin-8': 4,
 'string_violin-9': 4,
 'string_violin-10': 4,
 'string_violin-11': 4,
 'string_violin-12': 4,
 'string_violin-13': 4,
 'string_violin-14': 4,
 'string_violin-15': 4,
 'synth_bass-1': 3,
 'synth_bass-2': 3,
 'synth_bass-3': 3,
 'synth_bass-4': 3,
 'synth_bass-5': 3,
 'synth_bass-6': 3,
 'synth_bass-7': 3,
 'synth_bass-8': 3,
 'synth_bass-9': 3,
 'synth_bass-10': 3,
 'synth_bass-11': 3,
 'synth_bass-12': 3,
 'synth_bass-13': 3,
 'synth_bass-14': 3,
 'synth_bass-15': 3,
 'synth_bass_808-1': 3,
 'synth_bass_808-2': 3,
 'synth_bass_808-3': 3,
 'synth_bass_808-4': 3,
 'synth_bass_808-5': 3,
 'synth_bass_808-6': 3,
 'synth_bass_808-7': 3,
 'synth_bass_808-8': 3,
 'synth_bass_808-9': 3,
 'synth_bass_808-10': 3,
 'synth_bass_808-11': 3,
 'synth_bass_808-12': 3,
 'synth_bass_808-13': 3,
 'synth_bass_808-14': 3,
 'synth_bass_808-15': 3,
 'synth_bass_wobble-1': 3,
 'synth_bass_wobble-2': 3,
 'synth_bass_wobble-3': 3,
 'synth_bass_wobble-4': 3,
 'synth_bass_wobble-5': 3,
 'synth_bass_wobble-6': 3,
 'synth_bass_wobble-7': 3,
 'synth_bass_wobble-8': 3,
 'synth_bass_wobble-9': 3,
 'synth_bass_wobble-10': 3,
 'synth_bass_wobble-11': 3,
 'synth_bass_wobble-12': 3,
 'synth_bass_wobble-13': 3,
 'synth_bass_wobble-14': 3,
 'synth_bass_wobble-15': 3,
 'synth_bell-1': 2,
 'synth_bell-2': 2,
 'synth_bell-3': 2,
 'synth_bell-4': 2,
 'synth_bell-5': 2,
 'synth_bell-6': 2,
 'synth_bell-7': 2,
 'synth_bell-8': 2,
 'synth_bell-9': 2,
 'synth_bell-10': 2,
 'synth_bell-11': 2,
 'synth_bell-12': 2,
 'synth_bell-13': 2,
 'synth_bell-14': 2,
 'synth_bell-15': 2,
 'synth_lead-1': 1,
 'synth_lead-2': 1,
 'synth_lead-3': 1,
 'synth_lead-4': 1,
 'synth_lead-5': 1,
 'synth_lead-6': 1,
 'synth_lead-7': 1,
 'synth_lead-8': 1,
 'synth_lead-9': 1,
 'synth_lead-10': 1,
 'synth_lead-11': 1,
 'synth_lead-12': 1,
 'synth_lead-13': 1,
 'synth_lead-14': 1,
 'synth_lead-15': 1,
 'synth_pad-1': 4,
 'synth_pad-2': 4,
 'synth_pad-3': 4,
 'synth_pad-4': 4,
 'synth_pad-5': 4,
 'synth_pad-6': 4,
 'synth_pad-7': 4,
 'synth_pad-8': 4,
 'synth_pad-9': 4,
 'synth_pad-10': 4,
 'synth_pad-11': 4,
 'synth_pad-12': 4,
 'synth_pad-13': 4,
 'synth_pad-14': 4,
 'synth_pad-15': 4,
 'synth_pluck-1': 7,
 'synth_pluck-2': 7,
 'synth_pluck-3': 7,
 'synth_pluck-4': 7,
 'synth_pluck-5': 7,
 'synth_pluck-6': 7,
 'synth_pluck-7': 7,
 'synth_pluck-8': 7,
 'synth_pluck-9': 7,
 'synth_pluck-10': 7,
 'synth_pluck-11': 7,
 'synth_pluck-12': 7,
 'synth_pluck-13': 7,
 'synth_pluck-14': 7,
 'synth_pluck-15': 7,
 'synth_voice-1': 7,
 'synth_voice-2': 7,
 'synth_voice-3': 7,
 'synth_voice-4': 7,
 'synth_voice-5': 7,
 'synth_voice-6': 7,
 'synth_voice-7': 7,
 'synth_voice-8': 7,
 'synth_voice-9': 7,
 'synth_voice-10': 7,
 'synth_voice-11': 7,
 'synth_voice-12': 7,
 'synth_voice-13': 7,
 'synth_voice-14': 7,
 'synth_voice-15': 7,
 'timpani-1': 6,
 'timpani-2': 6,
 'timpani-3': 6,
 'timpani-4': 6,
 'timpani-5': 6,
 'timpani-6': 6,
 'timpani-7': 6,
 'timpani-8': 6,
 'timpani-9': 6,
 'timpani-10': 6,
 'timpani-11': 6,
 'timpani-12': 6,
 'timpani-13': 6,
 'timpani-14': 6,
 'timpani-15': 6,
 'trombone-1': 5,
 'trombone-2': 5,
 'trombone-3': 5,
 'trombone-4': 5,
 'trombone-5': 5,
 'trombone-6': 5,
 'trombone-7': 5,
 'trombone-8': 5,
 'trombone-9': 5,
 'trombone-10': 5,
 'trombone-11': 5,
 'trombone-12': 5,
 'trombone-13': 5,
 'trombone-14': 5,
 'trombone-15': 5,
 'trumpet-1': 5,
 'trumpet-2': 5,
 'trumpet-3': 5,
 'trumpet-4': 5,
 'trumpet-5': 5,
 'trumpet-6': 5,
 'trumpet-7': 5,
 'trumpet-8': 5,
 'trumpet-9': 5,
 'trumpet-10': 5,
 'trumpet-11': 5,
 'trumpet-12': 5,
 'trumpet-13': 5,
 'trumpet-14': 5,
 'trumpet-15': 5,
 'tuba-1': 5,
 'tuba-2': 5,
 'tuba-3': 5,
 'tuba-4': 5,
 'tuba-5': 5,
 'tuba-6': 5,
 'tuba-7': 5,
 'tuba-8': 5,
 'tuba-9': 5,
 'tuba-10': 5,
 'tuba-11': 5,
 'tuba-12': 5,
 'tuba-13': 5,
 'tuba-14': 5,
 'tuba-15': 5,
 'ukulele-1': 3,
 'ukulele-2': 3,
 'ukulele-3': 3,
 'ukulele-4': 3,
 'ukulele-5': 3,
 'ukulele-6': 3,
 'ukulele-7': 3,
 'ukulele-8': 3,
 'ukulele-9': 3,
 'ukulele-10': 3,
 'ukulele-11': 3,
 'ukulele-12': 3,
 'ukulele-13': 3,
 'ukulele-14': 3,
 'ukulele-15': 3,
 'vibraphone-1': 2,
 'vibraphone-2': 2,
 'vibraphone-3': 2,
 'vibraphone-4': 2,
 'vibraphone-5': 2,
 'vibraphone-6': 2,
 'vibraphone-7': 2,
 'vibraphone-8': 2,
 'vibraphone-9': 2,
 'vibraphone-10': 2,
 'vibraphone-11': 2,
 'vibraphone-12': 2,
 'vibraphone-13': 2,
 'vibraphone-14': 2,
 'vibraphone-15': 2,
 'whistle-1': 7,
 'whistle-2': 7,
 'whistle-3': 7,
 'whistle-4': 7,
 'whistle-5': 7,
 'whistle-6': 7,
 'whistle-7': 7,
 'whistle-8': 7,
 'whistle-9': 7,
 'whistle-10': 7,
 'whistle-11': 7,
 'whistle-12': 7,
 'whistle-13': 7,
 'whistle-14': 7,
 'whistle-15': 7,
 'xylophone-1': 2,
 'xylophone-2': 2,
 'xylophone-3': 2,
 'xylophone-4': 2,
 'xylophone-5': 2,
 'xylophone-6': 2,
 'xylophone-7': 2,
 'xylophone-8': 2,
 'xylophone-9': 2,
 'xylophone-10': 2,
 'xylophone-11': 2,
 'xylophone-12': 2,
 'xylophone-13': 2,
 'xylophone-14': 2,
 'xylophone-15': 2,
 'zither-1': 3,
 'zither-2': 3,
 'zither-3': 3,
 'zither-4': 3,
 'zither-5': 3,
 'zither-6': 3,
 'zither-7': 3,
 'zither-8': 3,
 'zither-9': 3,
 'zither-10': 3,
 'zither-11': 3,
 'zither-12': 3,
 'zither-13': 3,
 'zither-14': 3,
 'zither-15': 3,
 'orgel-1': 2,
 'orgel-2': 2,
 'orgel-3': 2,
 'orgel-4': 2,
 'orgel-5': 2,
 'orgel-6': 2,
 'orgel-7': 2,
 'orgel-8': 2,
 'orgel-9': 2,
 'orgel-10': 2,
 'orgel-11': 2,
 'orgel-12': 2,
 'orgel-13': 2,
 'orgel-14': 2,
 'orgel-15': 2,
 'synth_brass-1': 5,
 'synth_brass-2': 5,
 'synth_brass-3': 5,
 'synth_brass-4': 5,
 'synth_brass-5': 5,
 'synth_brass-6': 5,
 'synth_brass-7': 5,
 'synth_brass-8': 5,
 'synth_brass-9': 5,
 'synth_brass-10': 5,
 'synth_brass-11': 5,
 'synth_brass-12': 5,
 'synth_brass-13': 5,
 'synth_brass-14': 5,
 'synth_brass-15': 5,
 'sax-1': 5,
 'sax-2': 5,
 'sax-3': 5,
 'sax-4': 5,
 'sax-5': 5,
 'sax-6': 5,
 'sax-7': 5,
 'sax-8': 5,
 'sax-9': 5,
 'sax-10': 5,
 'sax-11': 5,
 'sax-12': 5,
 'sax-13': 5,
 'sax-14': 5,
 'sax-15': 5,
 'bamboo_flute-1': 5,
 'bamboo_flute-2': 5,
 'bamboo_flute-3': 5,
 'bamboo_flute-4': 5,
 'bamboo_flute-5': 5,
 'bamboo_flute-6': 5,
 'bamboo_flute-7': 5,
 'bamboo_flute-8': 5,
 'bamboo_flute-9': 5,
 'bamboo_flute-10': 5,
 'bamboo_flute-11': 5,
 'bamboo_flute-12': 5,
 'bamboo_flute-13': 5,
 'bamboo_flute-14': 5,
 'bamboo_flute-15': 5,
 'yanggeum-1': 3,
 'yanggeum-2': 3,
 'yanggeum-3': 3,
 'yanggeum-4': 3,
 'yanggeum-5': 3,
 'yanggeum-6': 3,
 'yanggeum-7': 3,
 'yanggeum-8': 3,
 'yanggeum-9': 3,
 'yanggeum-10': 3,
 'yanggeum-11': 3,
 'yanggeum-12': 3,
 'yanggeum-13': 3,
 'yanggeum-14': 3,
 'yanggeum-15': 3,
 'vocal-1': 8,
 'vocal-2': 8,
 'vocal-3': 8,
 'vocal-4': 8,
 'vocal-5': 8,
 'vocal-6': 8,
 'vocal-7': 8,
 'vocal-8': 8,
 'vocal-9': 8,
 'vocal-10': 8,
 'vocal-11': 8,
 'vocal-12': 8,
 'vocal-13': 8,
 'vocal-14': 8,
 'vocal-15': 8}

GENRE_MAP = {
    "newage": 0,
    "cinematic": 1,
}

TRACK_ROLE_MAP = {
    "main_melody": 0,
    "sub_melody": 1,
    "accompaniment": 2,
    "bass": 3,
    "pad": 4,
    "riff": 5,
}

RHYTHM_MAP = {
    "standard": 0,
    "triplet": 1,
}

