
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
from matplotlib.colors import SymLogNorm
import matplotlib.pyplot as plt
import numpy as np
from raysect.optical import World, Point3D, Vector3D, Spectrum
from raysect.optical.material import AbsorbingSurface
from jet.data import sal

# Internal imports
from cherab.core.utility import PhotonToJ
from cherab.core.atomic import Line, deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.openadas import OpenADAS
from cherab.tools.observers.group.plotting import select_pipelines
from cherab.solps import load_solps_from_mdsplus
from cherab.jet.machine import import_jet_mesh
from cherab.jet.spectroscopy.ks3 import load_ks3_inner_array, load_ks3_outer_array, array_polychromator


def plot_dalpha_emission(mesh, plasma, ks3_inner_array, ks3_outer_array):
    me = mesh.mesh_extent
    rl, ru = (me['minr'], me['maxr'])
    zl, zu = (me['minz'], me['maxz'])
    nr = 500
    nz = 1000
    rsamp = np.linspace(rl, ru, nr)
    zsamp = np.linspace(zl, zu, nz)
    emission = np.zeros((nz, nr))
    direction = Vector3D(0, 0, 1)
    for i, x in enumerate(rsamp):
        for j, z in enumerate(zsamp):
            point = Point3D(x, 0, z)
            spectrum = Spectrum(655., 657., 1)
            for model in plasma.models:
                emission[j, i] += model.emission(point, direction, spectrum).total()
    # plot emissivity
    fig, ax = plt.subplots(figsize=(5., 7.))
    linthresh = np.percentile(np.unique(emission), 1)
    norm = SymLogNorm(linthresh=linthresh)
    image = ax.imshow(emission, extent=[rl, ru, zl, zu], origin='lower', norm=norm)
    fig.colorbar(image, label='W m-3 sr-1', aspect=40)
    ax.set_xlim(rl, ru)
    ax.set_ylim(zl, zu)
    ax.set_xlabel('R [m]')
    ax.set_ylabel('Z [m]')

    # plot lines of sight
    length = 5.5
    for (los_group, color) in ((ks3_inner_array, '0.5'), (ks3_outer_array, '1.0')):
        for sight_line in los_group.observers:
            origin = sight_line.transform * Point3D(0, 0, 0)
            direction = sight_line.transform * Vector3D(0, 0, 1)
            radius = sight_line.radius
            dir_r = -np.sqrt(direction.x * direction.x + direction.y * direction.y)
            dir_z = direction.z
            obs_angle = np.arctan2(dir_z, dir_r)
            acc_angle = np.deg2rad(sight_line.acceptance_angle)
            shift_r_plus = -radius * np.sin(obs_angle)
            shift_z_plus = radius * np.cos(obs_angle)
            shift_r_minus = radius * np.sin(obs_angle)
            shift_z_minus = -radius * np.cos(obs_angle)
            dir_r_plus = np.cos(obs_angle + acc_angle)
            dir_z_plus = np.sin(obs_angle + acc_angle)
            dir_r_minus = np.cos(obs_angle - acc_angle)
            dir_z_minus = np.sin(obs_angle - acc_angle)
            ro = np.sqrt(origin.x**2 + origin.y**2)
            zo = origin.z
            re = ro + dir_r * length
            ze = zo + dir_z * length
            rplus = (ro + shift_r_plus, ro + shift_r_plus + dir_r_plus * length)
            rminus = (ro + shift_r_minus, ro + shift_r_minus + dir_r_minus * length)
            zplus = (zo + shift_z_plus, zo + shift_z_plus + dir_z_plus * length)
            zminus = (zo + shift_z_minus, zo + shift_z_minus + dir_z_minus * length)
            ax.plot(rplus, zplus, color=color, lw=0.75)
            ax.plot(rminus, zminus, color=color, lw=0.75)
            ax.plot((ro, re), (zo, ze), ls='--', color=color, lw=0.75)

    return ax


def load_ks3_pmt_array_data(pulse, time, signal, sequence=0, window=0.05):
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

ks3_inner = load_ks3_inner_array(pulse, instruments=[array_polychromator])
ks3_outer = load_ks3_outer_array(pulse, instruments=[array_polychromator])
ks3_inner.pixel_samples = 5000
ks3_outer.pixel_samples = 5000

# ----Plotting H-alpha emissivity and diagnostic geometry---- #

plt.ion()
ax = plot_dalpha_emission(sim.mesh, plasma, ks3_inner, ks3_outer)
ax.set_title('D-alpha emissivity (SOLPS #{} + ADAS),\nJET Pulse No. {}, time {} s'.format(ref_number, pulse, time))

# ----Observing with reflections---- #

world = World()
plasma.parent = world

# loading wall mesh
jet_mesh = import_jet_mesh(world)

pipeline_name = 'array_polychromator: D alpha'
radiance_refl_wall = {}
for los_group in (ks3_inner, ks3_outer):
    los_group.parent = world
    los_group.observe()
    pipelines, _ = select_pipelines(los_group, pipeline_name)
    radiance_refl_wall[los_group] = [pipeline.value.mean for pipeline in pipelines]

# ----Observing without reflections---- #

# changing wall material to AbsorbingSurface
absorbing_surface = AbsorbingSurface()
for mesh_component in jet_mesh:
    mesh_component.material = absorbing_surface

radiance_abs_wall = {}
for los_group in (ks3_inner, ks3_outer):
    los_group.observe()
    pipelines, _ = select_pipelines(los_group, pipeline_name)
    radiance_abs_wall[los_group] = [pipeline.value.mean for pipeline in pipelines]

# ----Reading the experimental values---- #

radiance_exp = {}
for (los_group, signal_name) in ((ks3_inner, 'dai'), (ks3_outer, 'dao')):
    radiance_photon = load_ks3_pmt_array_data(pulse, time, signal_name)
    radiance_exp[los_group] = PhotonToJ.to(radiance_photon, plasma.atomic_data.wavelength(deuterium, 0, (3, 2)))

# ----Plotting the results---- #

for los_group in (ks3_inner, ks3_outer):
    plt.figure()
    plt.plot(np.arange(1, 11), radiance_exp[los_group], color='k', ls='none', marker='s', mfc='none', label='Experiment')
    plt.plot(np.arange(1, 11), radiance_refl_wall[los_group], ls='none', marker='x', label='SOLPS with reflections')
    plt.plot(np.arange(1, 11), radiance_abs_wall[los_group], ls='none', marker='o', mfc='none', label='SOLPS without reflections')
    plt.text(0.97, 0.97, 'Pulse: {}\ntime: {} s'.format(pulse, time), transform=plt.gca().transAxes, ha='right', va='top')
    plt.legend(loc=2, frameon=False)
    plt.xlabel('Sight-line index')
    plt.ylabel('Observed Radiance, W sr-1 m-2')
    plt.title('D-alpha radiance on {} lines of sight'.format(los_group.name))

plt.ioff()
plt.show()
