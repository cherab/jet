
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


def load_kl11_voxel_grid(parent=None, name=None, active=None):

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

    voxel_grid = ToroidalVoxelGrid(voxel_coordinates, parent=parent, name=name, active=active)

    return voxel_grid


def load_old_kl11_voxel_grid(parent=None, name=None):

    import json

    directory = os.path.split(__file__)[0]
    voxel_grid_file = os.path.join(directory, "kl11_voxel_grid.json")

    with open(voxel_grid_file, 'r') as fh:
        grid_description = json.load(fh)

    voxel_coordinates = []
    for voxel in grid_description['cells']:
        v1 = Point2D(voxel['p1'][0], voxel['p1'][1])
        v2 = Point2D(voxel['p2'][0], voxel['p2'][1])
        v3 = Point2D(voxel['p3'][0], voxel['p3'][1])
        v4 = Point2D(voxel['p4'][0], voxel['p4'][1])
        voxel_coordinates.append((v1, v2, v3, v4))

    voxel_grid = ToroidalVoxelGrid(voxel_coordinates, parent=parent, name=name)

    return voxel_grid


def load_kl11_sensitivity_matrix(reflections=True):

    base_path = '/work/mcarr/tasks/kl11/data'
    camera_dimension = 334
    # grid_length = 7989
    grid_length = 2655

    sensitivity = np.zeros((grid_length, camera_dimension * camera_dimension))

    if reflections:
        for i in range(grid_length):
            sensitivity[i, :] = np.load(os.path.join(base_path, 'kl11_rf_sensitivity_matrix_{}.npy'.format(i))).flatten()
    else:
        for i in range(grid_length):
            sensitivity[i, :] = np.load(os.path.join(base_path, 'kl11_norf_sensitivity_matrix_{}.npy'.format(i))).flatten()

    return np.swapaxes(sensitivity, 0, 1)

