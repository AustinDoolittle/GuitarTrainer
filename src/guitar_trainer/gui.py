from dataclasses import dataclass
import tkinter as tk
from typing import Tuple

from guitar_trainer.music_utils import NOTE_TO_STRING, Note, STRING_TO_NOTES, MajorKey
from guitar_trainer.trainer import GuitarTrainer

GUITAR_STRING_SIZES = (8, 6, 5, 4, 3, 2)


@dataclass
class GuitarTrainerGuiRunParams:
    window_width: int = 2000
    window_height: int = 1000
    neck_width: int = 300
    nut_width: int = 25
    fret_width: int = 5
    fret_count: int = 14
    string_sizes: Tuple[int] = GUITAR_STRING_SIZES


@dataclass
class GuitarTrainerGuiColorParams:
    neck_color = '#d4a853'
    nut_color = '#362904'
    fret_color = '#4d4d4d'
    circle_color = "#000000"
    string_color = '#999999'
    note_circle_color = "#FEE12B"


@dataclass
class NoteCircle:
    circle_tk_id: int
    text_tk_id: int


class GuitarTrainerGui:
    def __init__(self, trainer: GuitarTrainer, color_params: GuitarTrainerGuiColorParams = GuitarTrainerGuiColorParams()):
        self.root = tk.Tk()
        self.canvas = None
        self.note_circles = None

        self.trainer = trainer

        self.color_params = color_params

    def _validate_run_params(self, params: GuitarTrainerGuiRunParams):
        if len(params.string_sizes) != self.trainer.num_strings:
            raise ValueError(f"Num strings reported by trainer ({self.trainer.num_strings()}) differs "
                             f"from string_sizes provided by params argument ({len(params.string_sizes)})")

    def _draw_circle(self, center_x, center_y, radius):
        return self.canvas.create_oval(center_x - radius, center_y - radius,
                                       center_x + radius, center_y + radius, fill=self.color_params.circle_color)

    def _modify_canvas_item(self, item_id, invisible=False, **kwargs):
        state = "hidden" if invisible else "normal"
        self.canvas.itemconfig(item_id, state=state, **kwargs)

    def _update_note_circle(self, note_circle: NoteCircle, note=None):
        default_kwargs = {
            "invisible": not bool(note)
        }
        self._modify_canvas_item(note_circle.circle_tk_id, fill=self.color_params.note_circle_color, **default_kwargs)
        self._modify_canvas_item(note_circle.text_tk_id, text=NOTE_TO_STRING.get(note, ""), **default_kwargs)
        self.canvas.tag_raise(note_circle.text_tk_id, note_circle.circle_tk_id)

    def _draw_frets(self, params: GuitarTrainerGuiRunParams, neck_upper, neck_lower):
        self._validate_run_params(params)

        # TODO make these spaced out like actual guitar neck
        spacing = (params.window_width - params.nut_width) / params.fret_count

        double_dot_space = 0
        single_dot_spaces = {3, 5, 7, 9}
        chromatic_scale_size = 12

        for fret_id in range(params.fret_count):
            fret_no = (fret_id + 1)

            fret_left = spacing * fret_no + params.nut_width - params.fret_width
            self.canvas.create_rectangle(
                fret_left, neck_lower, fret_left + params.fret_width, neck_upper, fill=self.color_params.fret_color)

            chromatic_scale_position = fret_no % chromatic_scale_size
            fret_wood_width = spacing - params.fret_width
            circle_radius = fret_wood_width / 8
            fret_wood_center_y = (params.window_height / 2)
            fret_wood_center_x = fret_left - fret_wood_width / 2

            if chromatic_scale_position == double_dot_space:
                vertical_center_offset = params.neck_width / 6

                # draw double dot
                self._draw_circle(fret_wood_center_x, fret_wood_center_y-vertical_center_offset, circle_radius)
                self._draw_circle(fret_wood_center_x, fret_wood_center_y+vertical_center_offset, circle_radius)
            elif chromatic_scale_position in single_dot_spaces:

                # draw single dot
                self._draw_circle(fret_wood_center_x, fret_wood_center_y, circle_radius)

    def _draw_strings(self, params: GuitarTrainerGuiRunParams, neck_upper, neck_lower):
        string_count = len(params.string_sizes)
        string_spacing = params.neck_width / string_count

        for i, string_width in enumerate(params.string_sizes):
            string_center_y = neck_upper - (string_spacing / 2) - string_spacing * i

            string_upper_y = string_center_y + (string_width / 2)
            string_lower_y = string_center_y - (string_width + 0.5 // 2)  # if odd, the lower side takes the extra pixel

            self.canvas.create_rectangle(
                params.nut_width, string_lower_y, params.window_width, string_upper_y,
                fill=self.color_params.string_color)

    def _draw_note_circles(self, params, neck_upper, neck_lower):
        fret_spacing = (params.window_width - params.nut_width) / params.fret_count
        fret_wood_width = fret_spacing - params.fret_width
        note_circle_radius = params.neck_width / 14
        string_spacing = params.neck_width / self.trainer.num_strings
        self.note_circles = []

        def _create_note_circle(x, y):
            note_circle_shape = self._draw_circle(x, y, note_circle_radius)
            note_circle_text = self.canvas.create_text(
                x, y, text="", fill="black", font='Helvetica 15 bold')
            return NoteCircle(note_circle_shape, note_circle_text)

        for i in range(self.trainer.num_strings):
            # draw the open string notes
            string_center_y = neck_upper - (string_spacing / 2) - string_spacing * i
            open_string_circle = _create_note_circle(note_circle_radius + 1, string_center_y)
            curr_string_note_circles = [open_string_circle]
            for fret_id in range(1, params.fret_count + 1):
                fret_left = fret_spacing * fret_id + params.nut_width - params.fret_width
                fret_wood_center_x = fret_left - fret_wood_width / 2

                note_circle = _create_note_circle(fret_wood_center_x, string_center_y)
                curr_string_note_circles.append(note_circle)

            self.note_circles.append(curr_string_note_circles)

    def _draw_neck(self, params: GuitarTrainerGuiRunParams):
        horizontal_middle = params.window_height / 2
        neck_lower = horizontal_middle - (params.neck_width / 2)
        neck_upper = horizontal_middle + (params.neck_width / 2)

        # draw neck background
        self.canvas.create_rectangle(0, neck_lower, params.window_width, neck_upper, fill=self.color_params.neck_color)

        # draw nut
        self.canvas.create_rectangle(0, neck_lower, params.nut_width, neck_upper, fill=self.color_params.nut_color)

        # draw frets
        self._draw_frets(params, neck_upper, neck_lower)
        self._draw_strings(params, neck_upper, neck_lower)
        self._draw_note_circles(params, neck_upper, neck_lower)

    def _update_note_circles(self, params):
        for string_id in range(self.trainer.num_strings):
            fret_notes = self.trainer.get_fret_notes_for_string(string_id, params.fret_count)
            for fret_id, note_circle in enumerate(self.note_circles[string_id]):
                self._update_note_circle(note_circle, fret_notes.get(fret_id))

    def _create_key_change_handler(self, params):
        def _handle_key_change(choice):
            note = STRING_TO_NOTES[choice]
            new_key = MajorKey(note)
            self.trainer.set_key(new_key)
            self._update_note_circles(params)

        return _handle_key_change

    def run(self, params: GuitarTrainerGuiRunParams):
        self.canvas = tk.Canvas(self.root, width=params.window_width, height=params.window_height)
        self.canvas.pack()

        key_string = tk.StringVar()
        key_string.set("Key: ")
        key_label = tk.Label(self.root, textvariable=key_string)
        key_label.pack()

        key_var = tk.StringVar()
        key_var.set("C")

        key_option = tk.OptionMenu(self.root, key_var, *[NOTE_TO_STRING[n] for n in list(Note)],
                                   command=self._create_key_change_handler(params))
        key_option.pack()

        self._draw_neck(params)
        self._update_note_circles(params)

        self.root.mainloop()
