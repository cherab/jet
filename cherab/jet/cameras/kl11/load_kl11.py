
import os
import csv
import numpy as np

from raysect.core import Point2D
from raysect.optical.observer import PowerPipeline2D, VectorCamera
from cherab.tools.observers import load_calcam_calibration
from cherab.tools.inversions import ToroidalVoxelGrid


def load_kl11_camera(parent=None, pipelines=None, stride=1):

    camera_config = load_calcam_calibration('/home/mcarr/cherab/cherab_jet/cherab/jet/cameras/kl11/KL11-E1DC_87516.nc')

    if not pipelines:
        power_unfiltered = PowerPipeline2D(display_unsaturated_fraction=0.96, name="Unfiltered Power (W)")
        power_unfiltered.display_update_time = 15
        pipelines = [power_unfiltered]

    pixels_shape, pixel_origins, pixel_directions = camera_config
    camera = VectorCamera(pixel_origins[::stride, ::stride], pixel_directions[::stride, ::stride],
                          pipelines=pipelines, parent=parent)
    camera.spectral_bins = 15
    camera.pixel_samples = 1

    return camera


def load_kl11_voxel_grid(parent=None, name=None):

    directory = os.path.split(__file__)[0]
    voxel_grid_file = os.path.join(directory, "kl11_voxel_grid.csv")

    voxel_coordinates = []
    with open(voxel_grid_file, 'r') as fh:
        reader = csv.reader(fh)

        for row in reader:
            v1 = Point2D(float(row[1]), float(row[2]))
            v2 = Point2D(float(row[3]), float(row[4]))
            v3 = Point2D(float(row[5]), float(row[6]))
            v4 = Point2D(float(row[7]), float(row[8]))
            voxel_coordinates.append((v1, v2, v3, v4))

    voxel_grid = ToroidalVoxelGrid(voxel_coordinates, parent=parent, name=name, primitive_type='csg')

    return voxel_grid


def load_kl11_sensitivity_matrix(camera='c', reflections=True):

    base_path = '/work/mcarr/tasks/kl11/data'
    camera_dimension = 334
    grid_length = 8893

    if camera == 'c':
        if reflections:
            sensitivity = np.load(os.path.join(base_path, 'kl11_c_rf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))
        else:
            sensitivity = np.load(os.path.join(base_path, 'kl11_c_norf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))

    elif camera == 'd':
        if reflections:
            sensitivity = np.load(os.path.join(base_path, 'kl11_d_rf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))
        else:
            sensitivity = np.load(os.path.join(base_path, 'kl11_d_norf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))

    elif camera == 'e':
        if reflections:
            sensitivity = np.load(os.path.join(base_path, 'kl11_e_rf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))
        else:
            sensitivity = np.load(os.path.join(base_path, 'kl11_e_norf_sensitivity_matrix.npy')).reshape((grid_length, camera_dimension * camera_dimension))

    else:
        raise ValueError("Unidentified KL11 camera - '{}'".format(camera))

    return np.swapaxes(sensitivity, 0, 1)

