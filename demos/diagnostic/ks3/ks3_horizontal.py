
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
import numpy as np
from raysect.optical import World, Spectrum
from raysect.optical.material import AbsorbingSurface

# Internal imports
from cherab.core.atomic import Line, deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
from cherab.solps import load_solps_from_mdsplus
from cherab.jet.machine import import_jet_mesh
from cherab.jet.spectroscopy.ks3 import load_ks3_bunker, load_ks3_horizontal_limiter, ksrb


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

ks3_bunker = load_ks3_bunker(pulse, instruments=[ksrb])
ks3_horizontal_limiter = load_ks3_horizontal_limiter(pulse, instruments=[ksrb])
ks3_bunker.accumulate = False
ks3_horizontal_limiter.accumulate = False
ks3_bunker.pixel_samples = 10000
ks3_horizontal_limiter.pixel_samples = 10000

# ----Observing with reflections---- #

world = World()
plasma.parent = world

# loading wall mesh
jet_mesh = import_jet_mesh(world)

radiance_refl_wall = {}
for sightline in (ks3_bunker, ks3_horizontal_limiter):
    sightline.parent = world
    sightline.observe()
    spectrum = Spectrum(ksrb.min_wavelength, ksrb.max_wavelength, ksrb.spectral_bins)
    spectrum.samples[:] = sightline.get_pipeline('ksrb').samples.mean
    radiance_refl_wall[sightline], = ksrb.calibrate(spectrum)

# ----Observing without reflections---- #

# changing wall material to AbsorbingSurface
absorbing_surface = AbsorbingSurface()
for mesh_component in jet_mesh:
    mesh_component.material = absorbing_surface

radiance_abs_wall = {}
for sightline in (ks3_bunker, ks3_horizontal_limiter):
    sightline.observe()
    spectrum.samples[:] = sightline.get_pipeline('ksrb').samples.mean
    radiance_abs_wall[sightline], = ksrb.calibrate(spectrum)

# ----Plotting the results---- #

for sightline in (ks3_bunker, ks3_horizontal_limiter):
    wavelength, = ksrb.wavelengths
    signal_share = 100 * radiance_abs_wall[sightline].sum() / radiance_refl_wall[sightline].sum()
    plt.figure()
    plt.plot(wavelength, radiance_refl_wall[sightline], color='k', label='Total signal')
    plt.plot(wavelength, radiance_abs_wall[sightline], ls='--', label='Useful signal ({:.1f}%)'.format(signal_share))
    plt.plot(wavelength, radiance_refl_wall[sightline] - radiance_abs_wall[sightline],
             ls=':', label='Stray light ({:.1f}%)'.format(100 - signal_share))
    plt.text(0.97, 0.97, 'Pulse: {}\ntime: {} s'.format(pulse, time), transform=plt.gca().transAxes, ha='right', va='top')
    plt.legend(loc=2, frameon=False)
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Spectral radiance [W sr-1 m-2 nm-1]')
    plt.title('D-alpha intensity on {} line of sight'.format(sightline.name))
    plt.xlim(655.4, 656.8)

plt.show()
