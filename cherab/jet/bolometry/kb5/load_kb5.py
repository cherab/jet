
import os
from cherab.tools.observers.bolometry import load_bolometer_camera
from cherab.tools.observers.inversion_grid import load_inversion_grid


_DATA_PATH = os.path.split(__file__)[0]


def load_kb5_camera(camera_id, parent=None, inversion_grid=None, extension='pickle'):

    if camera_id == 'KB5V':
        if extension == 'pickle':
            config_filename = 'kb5v_camera.pickle'
        elif extension == 'json':
            config_filename = 'kb5v_camera.json'
        else:
            raise ValueError("Unrecognised bolometer file extension '{}'.".format(extension))
    elif camera_id == 'KB5H':
        if extension == 'pickle':
            config_filename = 'kb5h_camera.pickle'
        elif extension == 'json':
            config_filename = 'kb5h_camera.json'
        else:
            raise ValueError("Unrecognised bolometer file extension '{}'.".format(extension))
    else:
        raise ValueError("Unrecognised bolometer camera_id '{}'.".format(camera_id))

    return load_bolometer_camera(os.path.join(_DATA_PATH, config_filename),
                                 parent=parent, inversion_grid=inversion_grid)


def load_kb5_inversion_grid():

    return load_inversion_grid(os.path.join(_DATA_PATH, "kb5_inversion_grid.json"))
