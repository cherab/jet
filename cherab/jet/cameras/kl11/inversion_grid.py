
import os

from cherab.tools.observers.inversion_grid import load_inversion_grid


def load_kl11_inversion_grid():

    directory = os.path.split(__file__)[0]

    return load_inversion_grid(os.path.join(directory, "kl11_inversion_grid.json"))
