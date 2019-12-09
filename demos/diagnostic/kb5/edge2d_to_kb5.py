#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt
from raysect.core import Point3D, Vector3D
from raysect.optical import Spectrum, World
from raysect.optical.material import AbsorbingSurface

from cherab.openadas import OpenADAS
from cherab.core.model import TotalRadiatedPower
from cherab.edge2d import load_edge2d_from_eproc
from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb5_camera


parser = argparse.ArgumentParser()
parser.add_argument('sim_path', help='The path to the edge2D simulation tran folder.')
parser.add_argument('-o', '--output', help='The name of an output file to which the data and a'
                    'figure image will be written (excluding file extensions).')
args = parser.parse_args()


world = World()
import_jet_mesh(world, override_material=AbsorbingSurface())

edge2d_sim = load_edge2d_from_eproc(args.sim_path)
# edge2d_sim = load_edge2d_from_eproc('/common/cmg/jsimpson/edge2d/runs/run1708151A/tran')
plasma = edge2d_sim.create_plasma(parent=world)
plasma.atomic_data = OpenADAS(missing_rates_return_null=True)

models = []
for species in plasma.composition:
    try:
        models.append(TotalRadiatedPower(species.element, species.charge))
    except ValueError:
        pass
plasma.models = models


plt.ion()
plt.figure()
xrange = np.linspace(0, 4, 200)
yrange = np.linspace(-2, 2, 200)
rad_rz_intensity = np.zeros((200, 200))
direction = Vector3D(0, 1, 0)
for i, x in enumerate(xrange):
    for j, y in enumerate(yrange):
        for model in models:
            emission = model.emission(Point3D(x, 0.0, y), direction, Spectrum(650, 660, 1))
            rad_rz_intensity[j, i] += emission.total()
plt.imshow(rad_rz_intensity, extent=[1.5, 4, -2, 2], origin='lower')
plt.colorbar()
plt.xlabel('r axis')
plt.ylabel('z axis')
plt.title("Total radiated power in R-Z [W/m^3/str]")


kb5v = load_kb5_camera('KB5V', parent=world, override_material=AbsorbingSurface())
kb5v_measurements = np.zeros((len(kb5v)))
for i, detector in enumerate(kb5v):
    detector.observe()
    kb5v_measurements[i] = detector.pipelines[0].value.mean

plt.figure()
plt.plot(kb5v_measurements)
plt.xlabel('Detector Index')
plt.ylabel('Measured Power [W]')
plt.title('Measured powers for KB5V')

kb5h = load_kb5_camera('KB5H', parent=world, override_material=AbsorbingSurface())
kb5h_measurements = np.zeros((len(kb5h)))
for i, detector in enumerate(kb5h):
    detector.observe()
    kb5h_measurements[i] = detector.pipelines[0].value.mean

plt.figure()
plt.plot(kb5h_measurements)
plt.xlabel('Detector Index')
plt.ylabel('Measured Power [W]')
plt.title('Measured powers for KB5H')

if args.output:
    np.save(args.output + '_kb5v', kb5v_measurements)
    np.save(args.output + '_kb5h', kb5h_measurements)

plt.ioff()
plt.show()
