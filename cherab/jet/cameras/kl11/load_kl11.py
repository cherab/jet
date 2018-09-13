
import os
import numpy as np

from raysect.optical.observer import PowerPipeline2D, VectorCamera
from cherab.tools.observers import load_calcam_calibration, load_inversion_grid


def load_kl11_camera(parent=None, pipelines=None, reduction_factor=1):

    camera_config = load_calcam_calibration('/home/mcarr/cherab/cherab_jet/cherab/jet/cameras/kl11/KL11-E1DC_87516.nc',
                                            reduction_factor=reduction_factor)

    if not pipelines:
        power_unfiltered = PowerPipeline2D(display_unsaturated_fraction=0.96, name="Unfiltered Power (W)")
        power_unfiltered.display_update_time = 15
        pipelines = [power_unfiltered]

    pixels_shape, pixel_origins, pixel_directions = camera_config
    camera = VectorCamera(pixel_origins, pixel_directions, pipelines=pipelines, parent=parent)
    camera.spectral_bins = 15
    camera.pixel_samples = 1

    return camera


def load_kl11_inversion_grid():

    directory = os.path.split(__file__)[0]

    return load_inversion_grid(os.path.join(directory, "kl11_inversion_grid.json"))


def load_kl11_sensitivity_matrix(reflections=True):

    base_path = '/work/mcarr/tasks/kl11/data'

    sensitivity = np.zeros((2655, 1000000))

    if reflections:
        for i in range(2655):
            sensitivity[i, :] = np.load(os.path.join(base_path, 'kl11_rf_sensitivity_matrix_{}.npy'.format(i))).flatten()
    else:
        for i in range(2655):
            sensitivity[i, :] = np.load(os.path.join(base_path, 'kl11_norf_sensitivity_matrix_{}.npy'.format(i))).flatten()

    return np.swapaxes(sensitivity, 0, 1)

