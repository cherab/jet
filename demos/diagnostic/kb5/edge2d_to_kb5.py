#!/usr/bin/env python
"""
This script demonstrates loading an EDGE2D simulation from a TRAN file
and forward-modelling the KB5 power profiles. Plasma emission is
modelled as the sum of the total radiated power from all species in the
simulation.

Running this demo requires some setup, as the cherab-edge2d package
(version 0.1.0 or later) and the EPROC routines must be available.
The former should be installed in the Python environment used to run
this script.
On the JET Data Centre (JDC) computers, the latter is available by
running the following commands:
```bash
module use /u/sim/jintrac/default/modules
module load jintrac
```
Important: you must load the jintrac module BEFORE activating any
virtual environments: the commands run during module activation may
overwrite certain environment variables (like PATH) set up by the
python virtual environment activation script and lead to
hard-to-diagnose issues.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
# Avoid segfault: see https://git.ccfe.ac.uk/jintrac/EPROC/-/issues/28
import eproc
_ = eproc.data('/common/cmg/jsimpson/edge2d/runs/run1708151A/tran', 'RMESH').data

from raysect.core import Point3D, Vector3D
from raysect.optical import Spectrum, World
from raysect.optical.material import AbsorbingSurface

from cherab.openadas import OpenADAS
from cherab.core.model import TotalRadiatedPower
from cherab.edge2d import load_edge2d_from_tranfile
from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb5_camera


parser = argparse.ArgumentParser()
parser.add_argument('sim_path', help='The path to the edge2D simulation tran folder,\n'
                    'e.g. "/common/cmg/jsimpson/edge2d/runs/run1708151A/tran".')
parser.add_argument('-o', '--output', help='The name of an output file to which the data and a'
                    'figure image will be written (excluding file extensions).')
args = parser.parse_args()


world = World()
import_jet_mesh(world, override_material=AbsorbingSurface())

edge2d_sim = load_edge2d_from_tranfile(args.sim_path)
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
xrange = np.linspace(1.5, 4, 200)
yrange = np.linspace(-2, 2, 200)
rad_rz_intensity = np.zeros((200, 200))
direction = Vector3D(0, 1, 0)
for i, x in enumerate(xrange):
    for j, y in enumerate(yrange):
        for model in models:
            emission = model.emission(Point3D(x, 0.0, y), direction, Spectrum(650, 660, 1))
            rad_rz_intensity[j, i] += emission.total()
plt.imshow(rad_rz_intensity, extent=[1.5, 4, -2, 2], origin='lower', cmap='Purples',
           norm=colors.LogNorm())
plt.colorbar()
plt.xlabel('r axis')
plt.ylabel('z axis')
plt.title("Total radiated power in R-Z [W/m^3/str]")
plt.pause(1)


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
plt.pause(1)

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
plt.pause(1)

if args.output:
    np.save(args.output + '_kb5v', kb5v_measurements)
    np.save(args.output + '_kb5h', kb5h_measurements)

plt.ioff()
plt.show()
