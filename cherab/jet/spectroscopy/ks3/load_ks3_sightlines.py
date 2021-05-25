
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

import numpy as np
from raysect.core import Point3D

from cherab.tools.observers import FibreOpticGroup, SpectroscopicFibreOptic
from .polychromator import array_polychromator, global_polychromator
from .spectrometer import ksra, ksrb, ksrc, ksrd
from .utility import reference_number


LOS_ORIGIN = {'inner': [Point3D(-0.012, 3.3345, 3.58845) for i in range(10)],
              'outer': [Point3D(-0.012, 2.7733, 3.606) for i in range(10)]}

LOS_END = {'inner': {80124: [Point3D(-0.075, 2.228, -1.6),
                             Point3D(-0.075, 2.273, -1.6),
                             Point3D(-0.075, 2.315, -1.6),
                             Point3D(-0.075, 2.363, -1.6),
                             Point3D(-0.075, 2.409, -1.6),
                             Point3D(-0.075, 2.453, -1.6),
                             Point3D(-0.075, 2.498, -1.6),
                             Point3D(-0.075, 2.542, -1.6),
                             Point3D(-0.075, 2.586, -1.6),
                             Point3D(-0.075, 2.631, -1.6)],
                     94115: [Point3D(-0.075, 2.289, -1.6),
                             Point3D(-0.075, 2.328, -1.6),
                             Point3D(-0.075, 2.366, -1.6),
                             Point3D(-0.075, 2.403, -1.6),
                             Point3D(-0.075, 2.413, -1.6),
                             Point3D(-0.075, 2.433, -1.6),
                             Point3D(-0.075, 2.480, -1.6),
                             Point3D(-0.075, 2.528, -1.6),
                             Point3D(-0.075, 2.584, -1.6),
                             Point3D(-0.075, 2.629, -1.6)]},
           'outer': {80124: [Point3D(-0.075, 2.521, -1.6),
                             Point3D(-0.075, 2.567, -1.6),
                             Point3D(-0.075, 2.611, -1.6),
                             Point3D(-0.075, 2.654, -1.6),
                             Point3D(-0.075, 2.697, -1.6),
                             Point3D(-0.075, 2.744, -1.6),
                             Point3D(-0.075, 2.787, -1.6),
                             Point3D(-0.075, 2.830, -1.6),
                             Point3D(-0.075, 2.886, -1.6),
                             Point3D(-0.075, 2.955, -1.6)],
                     94115: [Point3D(0.075, 2.619, -1.6),
                             Point3D(0.075, 2.664, -1.6),
                             Point3D(0.075, 2.702, -1.6),
                             Point3D(0.075, 2.743, -1.6),
                             Point3D(0.075, 2.786, -1.6),
                             Point3D(0.075, 2.830, -1.6),
                             Point3D(0.075, 2.874, -1.6),
                             Point3D(0.075, 2.910, -1.6),
                             Point3D(0.075, 2.962, -1.6),
                             Point3D(0.075, 3.019, -1.6)]}}

LOS_ORIGIN_RADIUS = {'inner': [0.0165 for i in range(10)],
                     'outer': [0.0165 for i in range(10)]}

LOS_END_RADIUS = {'inner': [0.025 for i in range(10)],
                  'outer': [0.025 for i in range(10)]}

KS3_INSTRUMENTS = {'inner': (array_polychromator, ksrc, ksrd),
                   'outer': (array_polychromator, ksra, ksrb),
                   'bunker': (ksra, ksrb),
                   'horizontal': (global_polychromator,),
                   'horizontal limiter': (ksrb,),
                   'vertical': (global_polychromator,),
                   'wide inner': (global_polychromator,),
                   'wide outer': (global_polychromator,)}


def _load_ks3_array(pulse, array_type, instrument=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner or outer lines of sight array.

    :param str array_type: 'inner' or 'outer'.
    :param SpectroscopicInstrument instrument: One of the KS3 inner array instruments:
                                               array_polychromator or ksrc or ksrd high-resolutoin
                                               spectrometers.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.
    """

    oldest_supported_pulse = min(LOS_END[array_type].keys())

    if pulse < oldest_supported_pulse:
        raise ValueError("Only shots >= {} are supported at this time.".format(oldest_supported_pulse))

    array_type = array_type.lower()

    if array_type not in ('inner', 'outer'):
        raise ValueError("Array type {} is not supported. Choose between 'inner' and 'outer'.".format(array_type))

    reference_pulse = reference_number(LOS_END[array_type], pulse)

    fibre_group = FibreOpticGroup(parent=parent, name='KS3 {} array'.format(array_type))

    for i in range(len(LOS_ORIGIN[array_type])):

        fibre_name = '{}'.format(i + 1)
        if fibre_names and fibre_name not in fibre_names:
            print('Skipped', fibre_name)
            continue

        fibre_direction = (LOS_ORIGIN[array_type][i].vector_to(LOS_END[array_type][reference_pulse][i]))
        acceptance_angle = np.rad2deg(np.arctan2(LOS_END_RADIUS[array_type][i] - LOS_ORIGIN_RADIUS[array_type][i], fibre_direction.length))
        fibre_direction_norm = fibre_direction.normalise()
        fibre = SpectroscopicFibreOptic(LOS_ORIGIN[array_type][i], fibre_direction_norm, name=fibre_name,
                                        acceptance_angle=acceptance_angle, radius=LOS_ORIGIN_RADIUS[array_type][i])

        fibre_group.add_sight_line(fibre)

    if instrument is None:
        # fibre_group.display_progress = False
        fibre_group.accumulate = False

        return fibre_group

    if instrument not in KS3_INSTRUMENTS[array_type]:
        raise ValueError("Only the following instruments are supported: {}. {} is given".format(KS3_INSTRUMENTS[array_type], instrument))

    fibre_group.connect_pipelines(instrument.pipeline_properties)
    fibre_group.accumulate = False
    # fibre_group.display_progress = False

    (fibre_group.min_wavelength,
     fibre_group.max_wavelength,
     fibre_group.spectral_bins) = instrument.wavelength_settings(pulse)

    return fibre_group


def load_ks3_inner_array(pulse, instrument=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner lines of sight array.

    :param SpectroscopicInstrument instrument: One of the KS3 inner array instruments:
                                               array_polychromator, ksrc and ksrd.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_array(pulse, 'inner', instrument=instrument, fibre_names=fibre_names, parent=parent)


def load_ks3_outer_array(pulse, instrument=None, fibre_names=None, parent=None):
    """
    Loads KS3 outer lines of sight array.

    :param SpectroscopicInstrument instrument: One of the KS3 outer array instruments:
                                               array_polychromator, ksra and ksrb.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_array(pulse, 'outer', instrument=instrument, fibre_names=fibre_names, parent=parent)
