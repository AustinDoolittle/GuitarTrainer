import enum
from dataclasses import dataclass
from typing import Tuple, List, Dict, Type

from guitar_trainer.music_utils import Key, MajorKey, Note, Tuning, StandardTuning


class Instrument(enum.Enum):
    GUITAR = "Guitar"
    BASS = "Bass"

    @classmethod
    def num_strings(cls, instrument: "Instrument"):
        if instrument == cls.GUITAR:
            return 6
        elif instrument == cls.BASS:
            return 4

        raise NotImplementedError()


@dataclass
class GuitarTrainerParams:
    default_key_cls: Type[Key] = MajorKey
    default_root_note: Note = Note.C
    default_tuning: Tuning = StandardTuning
    default_instrument: Instrument = Instrument.GUITAR


class GuitarTrainer:
    def __init__(self, params: GuitarTrainerParams):
        self.params = params

        self.instrument = self.params.default_instrument
        self.root_note = params.default_root_note
        self.key_cls = params.default_key_cls
        self.tuning = params.default_tuning

    def set_instrument(self, instrument: Instrument):
        self.instrument = instrument

    @property
    def num_strings(self):
        return Instrument.num_strings(self.instrument)

    def set_root_note(self, note: Note):
        self.root_note = note

    def set_tuning(self, tuning: Tuning):
        self.tuning = tuning

    def set_key(self, key_cls: Type[Key]):
        self.key_cls = key_cls

    def get_fret_notes_for_string(self, string_id, num_frets) -> Dict[int, Note]:
        if string_id >= self.num_strings or string_id < 0:
            raise ValueError(f"string_id of {string_id} is out of expected range [0 - {self.num_strings - 1}]")

        open_note = self.tuning.tuning[string_id]

        fret_notes = {}
        key = self.key_cls(self.root_note)
        for fret_id in range(num_frets + 1):
            curr_note = Note((open_note.value + fret_id) % len(Note))
            if curr_note not in key:
                continue

            fret_notes[fret_id] = curr_note

        return fret_notes
