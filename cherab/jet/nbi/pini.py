
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

import ppf
import re
import numpy as np

from raysect.core import Point3D, Vector3D, translate, rotate_basis
# from raysect.core.scenegraph.node import Node
from raysect.core import Node

from cherab.openadas import OpenADAS
from cherab.core.atomic.elements import deuterium
from cherab.core import Beam

from .idl_pini_geometry import get_pini_alignment


EDGE_WIDENING = 0.01
atomic_data = OpenADAS(permit_extrapolation=True)

PINI_LENGTHS = [16.10934611, 15.48338613, 11.57900764, 11.60077588, 11.47816349, 11.44278883, 15.90863813, 16.31158651]

OCTANT8_DEBUG_GEOMETRY = {
    1: {
        'position': Point3D(11.0386, -6.46009,  0.459),
        'direction': Vector3D(-0.925855, 0.376554, -0.0222852),
        'length': 16.10934611
    }, 2: {
        'position': Point3D(10.9539, -6.42668,  1.460),
        'direction': Vector3D(-0.925644, 0.374623, -0.1543590),
        'length': 15.48338613
    }, 3: {
        'position': Point3D(10.5227, -7.32298,  1.460),
        'direction': Vector3D(-0.863148, 0.476311, -0.1571810),
        'length': 11.57900764
    }, 4: {
        'position': Point3D(10.6114, -7.37055,  0.489),
        'direction': Vector3D(-0.864313, 0.478469, -0.0533585),
        'length': 11.60077588
    }, 5: {
        'position': Point3D(10.6114, -7.37055, -0.484),
        'direction': Vector3D(-0.872901, 0.484945,  0.0500080),
        'length': 11.47816349
    }, 6: {
        'position': Point3D(10.5227, -7.32298, -1.475),
        'direction': Vector3D(-0.873808, 0.483598,  0.1804630),
        'length': 11.44278883
    }, 7: {
        'position': Point3D(10.9539, -6.42668, -1.475),
        'direction': Vector3D(-0.916494, 0.369278,  0.1706620),
        'length': 15.90863813
    }, 8: {
        'position': Point3D(11.0386, -6.46009, -0.484),
        'direction': Vector3D(-0.912010, 0.368820,  0.0511293),
        'length': 16.31158651
    }
}

OCTANT8_DEBUG_ENERGIES = {
    1: {
        'energy': 109717./2,
        'powers': (1.17340e+06, 237300., 175050.)
    }, 2: {
        'energy': 109717./2,
        'powers': (1.19512e+06, 241693., 178290.)
    }, 3: {
        'energy': 100000./2,
        'powers': (0, 0, 0)
    }, 4: {
        'energy': 100000./2,
        'powers': (0, 0, 0)
    }, 5: {
        'energy': 109863./2,
        'powers': (1.08606e+06, 219749., 161481.)
    }, 6: {
        'energy': 109179./2,
        'powers': (1.00185e+06, 202222., 151293.)
    }, 7: {
        'energy': 99267.3/2,
        'powers': (1.02248e+06, 196378., 189440.)
    }, 8: {
        'energy': 99657.9/2,
        'powers': (1.00373e+06, 193255., 184596.)
    }
}


class JETPini(Node):
    """ Object representing a PINI in a scenegraph.

    Create a ready-to-observe PINI for charge-exchange spectroscopy.

    :param tuple pini_geometry: a tuple containing:
        * the source (Point3D),
        * the direction (Vector3D),
        * the divergence (tuple of two angles in degrees, horizontal then vertical),
        * the initial width (float in meters) and
        * the length (float in meters)
    of the PINI.
    :param tuple pini_parameters: a tuple containing:
        * the first component energy (float in eV/amu),
        * the power fractions (tuple of three fractions corresponding to decreasing energies, in W),
        * the turned on/turned modulation time vector (ndarray)
        * the species
    of the PINI.
    :param Plasma plasma:
    :param attenuation_instructions:
    :param emission_instructions:
    :param parent: the scenegraph parent, default is None.
    :param name:
    """

    def __init__(self, pini_geometry, pini_parameters, plasma, atomic_data, attenuator,
                 emission_models, integration_step=0.02, parent=None, name=""):

        source, direction, divergence, initial_width, length = pini_geometry
        energy, power_fractions, self._turned_on_func, element = pini_parameters

        self._components = []
        self._length = length
        self._parent_reminder = parent

        # Rotation between 'direction' and the z unit vector
        # This is important because the beam primitives are defined along the z axis.
        self._origin = source
        self._direction = direction
        direction.normalise()
        rotation = rotate_basis(direction, Vector3D(0., 0., 1.))
        transform_pini = translate(*source) * rotation

        Node.__init__(self,
                      parent=parent,
                      transform=transform_pini,
                      name=name)

        # the 3 energy components are different beams
        for comp_nb in [1, 2, 3]:

            beam = Beam(parent=self, transform=translate(0., 0., 0.), name="Beam component {}".format(comp_nb))
            beam.plasma = plasma
            beam.atomic_data = atomic_data
            beam.energy = energy / comp_nb
            beam.power = power_fractions[comp_nb - 1]
            beam.element = element
            # 1/e width is converted in standard deviation, assuming a gaussian shape.
            beam.sigma = initial_width / (2 * np.sqrt(2))
            # 1/e width divergences are converted in standard deviation divergences, assuming a gaussian shape.
            beam.divergence_x = np.arctan(np.tan(divergence[0]*np.pi/180.)/np.sqrt(2))
            beam.divergence_y = np.arctan(np.tan(divergence[1]*np.pi/180.)/np.sqrt(2))
            beam.length = length
            beam.attenuator = attenuator
            beam.models = emission_models
            beam.integrator.step = integration_step
            beam.integrator.min_samples = 10

            self._components.append(beam)

    @property
    def origin(self):
        return self._origin

    @property
    def direction(self):
        return self._direction

    @property
    def length(self):
        return self._length

    @property
    def components(self):
        return self._components

    @property
    def energy(self):
        return self._components[0].energy  # first component energy

    @energy.setter
    def energy(self, value):
        for i in range(3):
            component = self._components[i]
            component.energy = value / (i + 1)

    @property
    def power_fractions(self):
        return self._components[0].power, self._components[1].power, self._components[2].power

    @power_fractions.setter
    def power_fractions(self, value):
        for i in range(3):
            self._components[i].power = value[i]

    @property
    def power(self):
        total_power = 0.
        for component in self._components:
            total_power += component.power
        return total_power

    @property
    def turned_on(self):
        return self._turned_on

    @turned_on.setter
    def turned_on(self, value):
        if value:
            self.parent = self._parent_reminder
            self._turned_on = True
        else:
            self.parent = None
            self._turned_on = False

    def set_pini_time(self, time):
        """ Use the modulation waveform to set this pini on/off at the requested time.

        :param float time: The time at which to set this pini based on its modulation waveform.
        """
        self.turned_on = self._turned_on_func(time)

    @property
    def element(self):
        return self._components[0].element

    @element.setter
    def element(self, value):
        for component in self._components:
            component.element = value

    def emission_function(self, point, direction, spectrum):

        for beam in self._components:
            spectrum = beam.emission_function(point, direction, spectrum)

        return spectrum


def load_pini_from_ppf(shot, pini_id, plasma, atomic_data, attenuator, emission_models, world, integration_step=0.02):
    """
    Create a new JETPini instance for given pini ID from the NBI PPF settings.

    :param int shot: Shot number.
    :param pini_id: Code for pini to load.
    :param Plasma plasma: Plasma this pini will use for attenuation and emission calculations.
    :param attenuation_instructions:
    :param emission_instructions:
    :param world:
    :return: Loaded JET pini from PPF.
    """

    # TODO - get gas from ppf. Currently set to Deuterium only.

    if not re.match('^8.[1-8]$', pini_id):
        raise RuntimeError("JET Pini ID {} is invalid.".format(pini_id))

    octant, pini_index = pini_id.split('.')

    ###############################################
    # Load pini geometry from Carine's IDL routines

    # TODO - need to load pini geometry from a central location
    pini_geometry = get_pini_alignment(shot, int(pini_index))

    ########################################################
    # Load pini parameters from PPF -> assemble output tuple

    # first component energy (float in eV/amu)
    ppf.ppfuid('JETPPF', rw='R')
    ppf.ppfgo(pulse=shot, seq=0)
    _, _, data, _, _, ierr = ppf.ppfget(shot, 'NBI'+octant, 'ENG'+pini_index)
    if ierr != 0:
        raise OSError('No available NBI{}.{}'.format(octant, pini_index))

    energy = data[0] / deuterium.atomic_weight

    # tuple of three power fractions corresponding to decreasing energies, in W),
    _, _, data, _, _, _ = ppf.ppfget(shot, 'NBI'+octant, 'PFR'+pini_index)
    power_fractions = tuple(data)

    # Make an NBI masking function from NBL* power level time signal.
    _, _, data, _, t, _ = ppf.ppfget(shot, 'NBI'+octant, 'NBL'+pini_index)
    mask = np.empty(len(t), dtype=np.bool_)
    for i in range(len(t)):
        if data[i] > 250000:
            mask[i] = True
        else:
            mask[i] = False
    turned_on = TimeSeriesMask(mask, t)

    # Assemble tuple of pini parameters
    pini_parameters = (energy, power_fractions, turned_on, deuterium)

    # Construct JETPini and return
    return JETPini(pini_geometry, pini_parameters, plasma,
                   atomic_data, attenuator, emission_models, integration_step=integration_step, parent=world)


def load_debugging_pini(pini_id, plasma, atomic_data, attenuator, emission_models, world, integration_step=0.02):
    """
    Load a JET pini with preconfigured debugging settings.

    :param pini_id: Code for pini to load.
    :param Plasma plasma: Plasma this pini will use for attenuation and emission calculations.
    :param attenuation_instructions:
    :param emission_instructions:
    :param world:
    :return: Loaded JET pini from PPF.
    """

    if not re.match('^8.[1-8]$', pini_id):
        raise RuntimeError("JET Pini ID {} is invalid.".format(pini_id))

    octant, pini_index = pini_id.split('.')

    pid = int(pini_index)
    origin = OCTANT8_DEBUG_GEOMETRY[pid]['position']
    direction = OCTANT8_DEBUG_GEOMETRY[pid]['direction']
    divergence = (0.499995, 0.700488)
    initial_width = 0.001  # Approximate with 1mm as an effective point source.
    pini_length = OCTANT8_DEBUG_GEOMETRY[pid]['length']
    pini_geometry = (origin, direction, divergence, initial_width, pini_length)

    energy = OCTANT8_DEBUG_ENERGIES[pid]['energy']
    power_fractions = OCTANT8_DEBUG_ENERGIES[pid]['powers']
    turned_on = _dummy_time_series
    pini_parameters = (energy, power_fractions, turned_on, deuterium)

    # Construct JETPini and return
    return JETPini(pini_geometry, pini_parameters, plasma,
                   atomic_data, attenuator, emission_models, integration_step=integration_step, parent=world)


class TimeSeriesMask:

    def __init__(self, mask, time_axis):

        if len(mask) != len(time_axis):
            raise RuntimeError("Mask length must be equal to time_axis length.")
        self.mask = mask
        self.time_axis = time_axis

    def __call__(self, time):

        time_index = np.abs(self.time_axis - time).argmin()
        if self.mask[time_index]:
            return True
        else:
            return False

    def __iter__(self):

        for time_index in range(len(self.time_axis)):
            if self.mask[time_index]:
                yield self.time_axis[time_index]


def pini_time_series_from_ppf(pulse, pini_id):

    if not re.match('^8.[1-8]$', pini_id):
        raise RuntimeError("JET Pini ID {} is invalid.".format(pini_id))

    octant, pini_index = pini_id.split('.')

    # first component energy (float in eV/amu)
    ppf.ppfuid('JETPPF', rw='R')
    ppf.ppfgo(pulse=pulse, seq=0)

    _, _, data, _, t, _ = ppf.ppfget(pulse, 'NBI'+octant, 'NBL'+pini_index)
    mask = np.empty(len(t), dtype=np.bool_)
    for i in range(len(t)):
        if data[i] > 250000:
            mask[i] = True
        else:
            mask[i] = False

    return TimeSeriesMask(mask, t)


def _dummy_time_series(time):
    return True



