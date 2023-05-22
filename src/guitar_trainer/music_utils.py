import abc
import enum


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


GUITAR_STANDARD_TUNING = (Note.E, Note.A, Note.D, Note.G, Note.B, Note.E)


class Key(abc.ABC):
    @abc.abstractmethod
    def get_notes(self):
        raise NotImplementedError()

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
    _NOTES = list(Note)

    def get_notes(self):
        return self._NOTES


class MajorKey(Key):
    SPACING = (2, 2, 1, 2, 2, 2)

    def __init__(self, note: Note):
        self._notes = self._get_notes_with_spacing(note, self.SPACING)

    def get_notes(self):
        return self._notes


class MinorKey(Key):
    SPACING = (2, 1, 2, 2, 1, 2)

    def __init__(self, note: Note):
        self._notes = self._get_notes_with_spacing(note, self.SPACING)

    def get_notes(self):
        return self._notes
