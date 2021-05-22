
# Copyright 2014-2017 United Kingdom Atomic Energy Authority
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

# External imports
import matplotlib.pyplot as plt
import numpy as np
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface
from jet.data import sal

# Internal imports
from cherab.core.utility import PhotonToJ
from cherab.core.atomic import Line, deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
from cherab.solps import load_solps_from_mdsplus
from cherab.jet.machine import import_jet_mesh
from cherab.jet.spectroscopy.ks3 import load_ks3_inner_array, load_ks3_outer_array, array_polychromator


def load_ks3_pmt_array_data(pulse, time, signal, sequence=0, window=0.1):
    data = sal.get('/pulse/{}/ppf/signal/jetppf/edg8/{}:{}'.format(pulse, signal, sequence))
    t = data.dimensions[0].data
    it_min = np.abs(t - time + 0.5 * window).argmin()  # closest time moment
    it_max = np.abs(t - time - 0.5 * window).argmin()  # closest time moment

    return data.data[it_min:it_max].mean(0) * 1.e4  # cm-2 --> m-2


# ----Creating plasma from SOLPS simulation---- #
mds_server = 'solps-mdsplus.aug.ipp.mpg.de:8001'
ref_number = 125237
pulse = 90512
time = 49.6

sim = load_solps_from_mdsplus(mds_server, ref_number)
plasma = sim.create_plasma()
plasma.atomic_data = OpenADAS(permit_extrapolation=True)
plasma.integrator.step = 0.005

# ----Adding Gaussian D-alpha line shape model---- #
d_alpha = Line(deuterium, 0, (3, 2))
plasma.models = [ExcitationLine(d_alpha), RecombinationLine(d_alpha)]

# ----Loading diagnostics---- #
ks3 = {'inner': load_ks3_inner_array(pulse, instrument=array_polychromator),
       'outer': load_ks3_outer_array(pulse, instrument=array_polychromator)}
ks3['inner'].pixel_samples = 5000
ks3['outer'].pixel_samples = 5000

# ----Observing without reflections---- #

world = World()
plasma.parent = world

# loading wall mesh
import_jet_mesh(world, override_material=AbsorbingSurface())

radiance_abs_wall = {}
for los_array_type in ('inner', 'outer'):
    ks3[los_array_type].parent = world
    ks3[los_array_type].observe()
    radiance_abs_wall[los_array_type] = [sightline.observed_spectrum(0).total() for sightline in ks3[los_array_type].sight_lines]

# ----Observing with reflections---- #

world = World()
plasma.parent = world

# loading wall mesh
import_jet_mesh(world)

radiance_refl_wall = {}
for los_array_type in ('inner', 'outer'):
    ks3[los_array_type].parent = world
    ks3[los_array_type].observe()
    radiance_refl_wall[los_array_type] = [sightline.observed_spectrum(0).total() for sightline in ks3[los_array_type].sight_lines]

# ----Reading the experimental values---- #

radiance_exp = {}
for los_array_type in ('inner', 'outer'):
    radiance_photon = load_ks3_pmt_array_data(pulse, time, 'da{}'.format(los_array_type[0]))
    radiance_exp[los_array_type] = PhotonToJ.to(radiance_photon, plasma.atomic_data.wavelength(deuterium, 0, (3, 2)))

# ----Plotting the results---- #

for los_array_type in ('inner', 'outer'):
    plt.figure()
    plt.plot(np.arange(1, 11), radiance_exp[los_array_type], color='k', ls='none', marker='s', mfc='none', label='Experiment')
    plt.plot(np.arange(1, 11), radiance_refl_wall[los_array_type], ls='none', marker='x', label='SOLPS with reflections')
    plt.plot(np.arange(1, 11), radiance_abs_wall[los_array_type], ls='none', marker='o', mfc='none', label='SOLPS without reflections')
    plt.text(0.97, 0.97, 'Pulse: {}\ntime: {} s'.format(pulse, time), transform=plt.gca().transAxes, ha='right', va='top')
    plt.legend(loc=2, frameon=False)
    plt.xlabel('Sight-line index')
    plt.ylabel('Observed Radiance, W sr-1 m-2')
    plt.title('D-alpha radiance across KS3 {} sight-lines'.format(los_array_type))

plt.show()
