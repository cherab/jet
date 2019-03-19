#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt
from raysect.core import Point3D, Vector3D
from raysect.core.math.function.function3d import PythonFunction3D
from raysect.optical import Spectrum

from cherab.core.atomic import deuterium, carbon, Line
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
from cherab.edge2d import load_edge2d_from_eproc
from cherab.jet.cameras.kl11 import load_kl11_voxel_grid, load_kl11_sensitivity_matrix, load_kl11_camera


available_lines = {
    'd-alpha': Line(deuterium, 0, (3, 2)),
    'd_beta': Line(deuterium, 0, (4, 2)),
    'd-gamma': Line(deuterium, 0, (5, 2)),
    'd_delta': Line(deuterium, 0, (6, 2)),
    'd_epsilon': Line(deuterium, 0, (7, 2))
    'ciii_465': Line(carbon, 2, ('2s1 3p1 3P4.0', '2s1 3s1 3S1.0'))
}

parser = argparse.ArgumentParser()
parser.add_argument('sim_path', help='The path to the edge2D simulation tran folder.')
parser.add_argument('-c', '--camera', help='The camera id which will be simulated must be one of'
                    '[a, b, c, d].', default='c')
parser.add_argument('-l', '--line', help='The emission line that will be simulated.',
                    choices=list(available_lines.keys()), default='d-alpha')
parser.add_argument('-o', '--output', help='The name of an output file to which the data and an'
                    'image will be written (excluding file extensions).')
args = parser.parse_args()


sensitivity = load_kl11_sensitivity_matrix(camera='c')
voxel_grid = load_kl11_voxel_grid()
camera = load_kl11_camera(stride=3)


edge2d_sim = load_edge2d_from_eproc(args.sim_path)
# edge2d_sim = load_edge2d_from_eproc('/common/cmg/jsimpson/edge2d/runs/run1708151A/tran')
plasma = edge2d_sim.create_plasma()
plasma.atomic_data = OpenADAS()

excitation_model = ExcitationLine(available_lines[args.line])
# excitation_model = ExcitationLine(available_lines['d-alpha'])
recombination_model = RecombinationLine(available_lines[args.line])
# recombination_model = RecombinationLine(available_lines['d-alpha'])
plasma.models = [excitation_model, recombination_model]


class EmissionFunction(PythonFunction3D):

    def __init__(self, model):

        self.model = model

    def __call__(self, x, y, z):

        direction = Vector3D(1, 0, 0)
        spectrum = Spectrum(400, 750, 1)
        observed = self.model.emission(Point3D(x, y, z), direction, spectrum)

        return observed.total()


excit_func = EmissionFunction(excitation_model)
recom_func = EmissionFunction(recombination_model)

emissivities = voxel_grid.emissivities_from_function(excit_func)
emissivities += voxel_grid.emissivities_from_function(recom_func)

synthetic_image = np.matmul(sensitivity, emissivities).reshape(camera.pixels)

plt.ion()
voxel_grid.plot(voxel_values=emissivities)
plt.title('Line emissivity - {}'.format(args.line))
if args.output:
    plt.savefig(args.output + '_emissivity.png')

plt.figure()
plt.imshow(synthetic_image, cmap='gray')
plt.colorbar()
plt.title('KL11 - Synthetic Image')
if args.output:
    plt.savefig(args.output + '.png')
    np.save(args.output, synthetic_image)

plt.ioff()
plt.show()
