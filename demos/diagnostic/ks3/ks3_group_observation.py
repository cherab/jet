
# Copyright 2014-2021 United Kingdom Atomic Energy Authority
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
from raysect.optical import World

# Internal imports
from cherab.core.atomic import Line, deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
from cherab.tools.observers.group.plotting import plot_group_total, plot_group_spectra
from cherab.solps import load_solps_from_mdsplus
from cherab.jet.machine import import_jet_mesh
from cherab.jet.spectroscopy.ks3 import load_ks3_outer_array, array_polychromator, ksrb


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

# ----Loading wall mesh---- #
world = World()
import_jet_mesh(world)

# ----Loading diagnostics---- #

# KS3 outer array with polychromator and KSRB high-resolution spectrometer
ks3_outer = load_ks3_outer_array(pulse, instruments=[array_polychromator, ksrb], parent=world)
ks3_outer.pixel_samples = 5000

# ----Observing---- #

plasma.parent = world

ks3_outer.observe()

# ----Plotting the results---- #

plot_group_total(ks3_outer, item='array_polychromator: D alpha')

ax = plot_group_spectra(ks3_outer, item='ksrb', in_photons=True)
ax.set_xlim(655.6, 656.6)

plot_group_total(ks3_outer, item='ksrb')

plt.show()
