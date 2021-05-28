
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
from raysect.optical import World

# Internal imports
from cherab.core.atomic import Line, deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
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

# polychromator
ks3_inner_poly = load_ks3_outer_array(pulse, instrument=array_polychromator, parent=world)
ks3_inner_poly.pixel_samples = 5000

# high-resolution spectrometer
ks3_inner_hrs = load_ks3_outer_array(pulse, instrument=ksrb, parent=world)
ks3_inner_hrs.pixel_samples = 5000

# ----Observing---- #

plasma.parent = world

ks3_inner_poly.observe()
ks3_inner_hrs.observe()

# ----Plotting the results---- #

ks3_inner_poly.plot_total_signal('D alpha (PMT)')

ax = ks3_inner_hrs.plot_spectra('ksrb', in_photons=True)
ax.set_xlim(655.6, 656.6)

ks3_inner_hrs.plot_total_signal('ksrb')

plt.show()
