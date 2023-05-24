import abc
import enum
from dataclasses import dataclass
from typing import List, Union, Optional


class Note(enum.Enum):
    A = 0
    A_SH = 1
    B = 2
    C = 3
    C_SH = 4
    D = 5
    D_SH = 6
    E = 7
    F = 8
    F_SH = 9
    G = 10
    G_SH = 11


NOTE_TO_STRING = {
    Note.A: "A",
    Note.A_SH: "A#",
    Note.B: "B",
    Note.C: "C",
    Note.C_SH: "C#",
    Note.D: "D",
    Note.D_SH: "D#",
    Note.E: "E",
    Note.F: "F",
    Note.F_SH: "F#",
    Note.G: "G",
    Note.G_SH: "G#"
}

STRING_TO_NOTES = {
    val: key for key, val in NOTE_TO_STRING.items()
}


@dataclass
class Tuning:
    name: str
    tuning: List[Note]


StandardTuning = Tuning("Standard", [Note.E, Note.A, Note.D, Note.G, Note.B, Note.E])
KorbinsTuning = Tuning("Korbins", [Note.D, Note.A, Note.E, Note.A, Note.C_SH, Note.E])
GUITAR_TUNINGS = {t.name: t for t in (StandardTuning, KorbinsTuning)}


class Key(abc.ABC):
    def __init__(self, root_note: Optional[Note], **kwargs):
        super().__init__(**kwargs)
        self._root_note = root_note
        self._notes = self._get_notes_with_spacing(root_note, self.spacing)

    @classmethod
    @abc.abstractmethod
    def name(cls):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def spacing(self) -> List[int]:
        raise NotImplementedError()

    @property
    def root_note(self):
        return self._root_note

    def get_notes(self):
        return self._notes

    @classmethod
    def _get_notes_with_spacing(cls, root_note, spacing):
        note_id = root_note.value
        notes = [root_note]
        offset = 0
        for spacing in spacing:
            offset += spacing
            new_note = Note((note_id + offset) % len(Note))
            notes.append(new_note)

        return notes

    def __contains__(self, item):
        # NOTE O(N) lookup, but unlikely to be a bottleneck
        return item in self.get_notes()


class ChromaticKey(Key):
    @classmethod
    def name(cls):
        return "Chromatic"

    @property
    def spacing(self) -> List[int]:
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


class MajorKey(Key):
    @classmethod
    def name(cls):
        return "Major"

    @property
    def spacing(self) -> List[int]:
        return [2, 2, 1, 2, 2, 2]


class MinorKey(Key):
    @classmethod
    def name(cls):
        return "Minor"

    @property
    def spacing(self) -> List[int]:
        return [2, 1, 2, 2, 1, 2]


KEYS = {k.name(): k for k in (ChromaticKey, MajorKey, MinorKey)}
