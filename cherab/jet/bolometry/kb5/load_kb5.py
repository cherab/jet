
import os
from cherab.tools.observers.bolometry import load_bolometer_camera


_DATA_PATH = os.path.split(__file__)[0]


def load_KB5(camera_id, parent=None, inversion_grid=None):

    if camera_id == 'KB5V':
        config_filename = 'KB5V_camera.json'
    else:
        raise ValueError("Unrecognised bolometer camera_id '{}'.".format(camera_id))

    return load_bolometer_camera(os.path.join(_DATA_PATH, config_filename),
                                 parent=parent, inversion_grid=inversion_grid)
