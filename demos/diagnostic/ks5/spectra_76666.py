
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
import numpy as np
from scipy.constants import electron_mass, atomic_mass
from jet.data import sal
from raysect.core import Vector3D
from raysect.optical import World

# Internal imports
from cherab.core.math import Interpolate1DCubic, IsoMapper2D, IsoMapper3D, AxisymmetricMapper, Blend2D, Constant2D, VectorAxisymmetricMapper
from cherab.core import Plasma, Maxwellian, Species
from cherab.core.atomic import Line, deuterium, carbon
from cherab.core.model import SingleRayAttenuator, BeamCXLine
from cherab.openadas import OpenADAS
from cherab.jet.nbi import load_pini_from_ppf
from cherab.jet.equilibrium import JETEquilibrium
from cherab.jet.spectroscopy.ks5 import load_ks5_sightlines


PULSE = 79666
PULSE_PLASMA = 79503  # /!\ Plasma configuration is from pulse 79503!
TIME = 61.0

world = World()

adas = OpenADAS(permit_extrapolation=True)  # create atomic data source


# ########################### PLASMA EQUILIBRIUM ############################ #
print('Plasma equilibrium')

equilibrium = JETEquilibrium(PULSE)
equil_time_slice = equilibrium.time(TIME)
psin_2d = equil_time_slice.psi_normalised
psin_3d = AxisymmetricMapper(equil_time_slice.psi_normalised)
inside_lcfs = equil_time_slice.inside_lcfs


# ########################### PLASMA CONFIGURATION ########################## #
print('Plasma configuration')

plasma = Plasma(parent=world)
plasma.atomic_data = adas
plasma.b_field = VectorAxisymmetricMapper(equil_time_slice.b_field)

DATA_PATH = '/pulse/{}/ppf/signal/{}/{}/{}:{}'
user = 'cgiroud'
sequence = 0

psi_coord = sal.get(DATA_PATH.format(PULSE_PLASMA, user, 'PRFL', 'C6', sequence)).dimensions[0].data
mask = psi_coord <= 1.0
psi_coord = psi_coord[mask]

flow_velocity_tor_data = sal.get(DATA_PATH.format(PULSE_PLASMA, user, 'PRFL', 'VT', sequence)).data[mask]
flow_velocity_tor_psi = Interpolate1DCubic(psi_coord, flow_velocity_tor_data)
flow_velocity_tor = AxisymmetricMapper(Blend2D(Constant2D(0.0), IsoMapper2D(psin_2d, flow_velocity_tor_psi), inside_lcfs))
flow_velocity = lambda x, y, z: Vector3D(y * flow_velocity_tor(x, y, z), - x * flow_velocity_tor(x, y, z), 0.) \
                                / np.sqrt(x*x + y*y)

ion_temperature_data = sal.get(DATA_PATH.format(PULSE_PLASMA, user, 'PRFL', 'TI', sequence)).data[mask]
print("Ti between {} and {} eV".format(ion_temperature_data.min(), ion_temperature_data.max()))
ion_temperature_psi = Interpolate1DCubic(psi_coord, ion_temperature_data)
ion_temperature = AxisymmetricMapper(Blend2D(Constant2D(0.0), IsoMapper2D(psin_2d, ion_temperature_psi), inside_lcfs))

electron_density_data = sal.get(DATA_PATH.format(PULSE_PLASMA, user, 'PRFL', 'NE', sequence)).data[mask]
print("Ne between {} and {} m-3".format(electron_density_data.min(), electron_density_data.max()))
electron_density_psi = Interpolate1DCubic(psi_coord, electron_density_data)
electron_density = AxisymmetricMapper(Blend2D(Constant2D(0.0), IsoMapper2D(psin_2d, electron_density_psi), inside_lcfs))

density_c6_data = sal.get(DATA_PATH.format(PULSE_PLASMA, user, 'PRFL', 'C6', sequence)).data[mask]
density_c6_psi = Interpolate1DCubic(psi_coord, density_c6_data)
density_c6 = AxisymmetricMapper(Blend2D(Constant2D(0.0), IsoMapper2D(psin_2d, density_c6_psi), inside_lcfs))
density_d = lambda x, y, z: electron_density(x, y, z) - 6 * density_c6(x, y, z)

d_distribution = Maxwellian(density_d, ion_temperature, flow_velocity, deuterium.atomic_weight * atomic_mass)
c6_distribution = Maxwellian(density_c6, ion_temperature, flow_velocity, carbon.atomic_weight * atomic_mass)
e_distribution = Maxwellian(electron_density, ion_temperature, flow_velocity, electron_mass)

d_species = Species(deuterium, 1, d_distribution)
c6_species = Species(carbon, 6, c6_distribution)

plasma.electron_distribution = e_distribution
plasma.composition = [d_species, c6_species]



# ########################### NBI CONFIGURATION ############################# #

print('Loading JET PINI configuration...')

beam_attenuator = SingleRayAttenuator(clamp_to_zero=True)
beam_emission_models = [BeamCXLine(Line(carbon, 5, (8, 7)))]

pini_8_1 = load_pini_from_ppf(PULSE, '8.1', plasma, adas, beam_attenuator, beam_emission_models, world)
pini_8_2 = load_pini_from_ppf(PULSE, '8.2', plasma, adas, beam_attenuator, beam_emission_models, world)
pini_8_5 = load_pini_from_ppf(PULSE, '8.5', plasma, adas, beam_attenuator, beam_emission_models, world)
pini_8_6 = load_pini_from_ppf(PULSE, '8.6', plasma, adas, beam_attenuator, beam_emission_models, world)


# ############################### OBSERVATION ############################### #
print('Observation')

ks5c = load_ks5_sightlines(PULSE, 'ks5c', parent=world)

ks5c.observe()


