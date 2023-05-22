import enum
from dataclasses import dataclass
from typing import Tuple, List, Dict

from guitar_trainer.music_utils import Key, MajorKey, Note, GUITAR_STANDARD_TUNING


@dataclass
class GuitarTrainerParams:
    default_key: Key = MajorKey(Note.C)
    default_tuning: Tuple[Note] = GUITAR_STANDARD_TUNING


class GuitarTrainer:
    def __init__(self, params: GuitarTrainerParams):
        self.params = params

        self.key = params.default_key
        self.tuning = params.default_tuning

    @property
    def num_strings(self):
        return len(self.params.default_tuning)

    def set_key(self, key: Key):
        self.key = key

    def get_fret_notes_for_string(self, string_id, num_frets) -> Dict[int, Note]:
        if string_id >= self.num_strings or string_id < 0:
            raise ValueError(f"string_id of {string_id} is out of expected range [0 - {self.num_strings-1}]")

        open_note = self.tuning[string_id]

        fret_notes = {}
        for fret_id in range(num_frets + 1):
            curr_note = Note((open_note.value + fret_id) % len(Note))
            if curr_note not in self.key:
                continue

            fret_notes[fret_id] = curr_note

        return fret_notes
