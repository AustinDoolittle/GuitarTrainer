import sys

from guitar_trainer.music_utils import MinorKey, Note
from guitar_trainer.trainer import GuitarTrainer, GuitarTrainerParams
from guitar_trainer.gui import GuitarTrainerGui, GuitarTrainerGuiRunParams


def main(argv):
    trainer_params = GuitarTrainerParams()
    guitar_trainer = GuitarTrainer(trainer_params)
    gui = GuitarTrainerGui(guitar_trainer)

    params = GuitarTrainerGuiRunParams()
    gui.run(params)


if __name__ == "__main__":
    main(sys.argv[1:])
