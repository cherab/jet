
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

from cherab.tools.observers import FibreOpticGroup, SpectroscopicFibreOptic
from .utility import reference_number
from .sightline_parameters import KS3_LOS_PARAMETERS


def _load_ks3_array(pulse, array_type, instrument=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner or outer lines of sight array.

    :param int pulse: JET pulse number.
    :param str array_type: 'inner' or 'outer'.
    :param SpectroscopicInstrument instrument: One of the KS3 inner array instruments:
                                               array_polychromator or ksrc or ksrd high-resolutoin
                                               spectrometers.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.
    """

    array_type = array_type.lower()
    if array_type not in ('inner', 'outer'):
        raise ValueError("Array type {} is not supported. Choose between 'inner' and 'outer'.".format(array_type))

    parameters = KS3_LOS_PARAMETERS[array_type]

    oldest_supported_pulse = min(parameters.keys())

    if pulse < oldest_supported_pulse:
        raise ValueError("Only shots >= {} are supported at this time.".format(oldest_supported_pulse))

    reference_pulse = reference_number(parameters, pulse)

    fibre_group = FibreOpticGroup(parent=parent, name='KS3 {} array'.format(array_type))

    origin = parameters[reference_pulse]['origin']
    end = parameters[reference_pulse]['end']
    origin_radius = parameters[reference_pulse]['origin_radius']
    end_radius = parameters[reference_pulse]['end_radius']
    instruments = parameters[reference_pulse]['instruments']

    for i in range(len(origin)):

        fibre_name = '{}'.format(i + 1)
        if fibre_names and fibre_name not in fibre_names:
            print('Skipped', fibre_name)
            continue

        fibre_direction = origin[i].vector_to(end[i])
        acceptance_angle = np.rad2deg(np.arctan2(end_radius[i] - origin_radius[i], fibre_direction.length))
        fibre_direction_norm = fibre_direction.normalise()
        fibre = SpectroscopicFibreOptic(origin[i], fibre_direction_norm, name=fibre_name,
                                        acceptance_angle=acceptance_angle, radius=origin_radius[i])

        fibre_group.add_sight_line(fibre)

    if instrument is None:

        return fibre_group

    if instrument not in instruments:
        intrument_names = ', '.join(instr.name for instr in instruments)
        raise ValueError("Only the following instruments are supported: {}.".format(intrument_names))

    fibre_group.connect_pipelines(instrument.pipeline_properties)

    (fibre_group.min_wavelength,
     fibre_group.max_wavelength,
     fibre_group.spectral_bins) = instrument.wavelength_settings(pulse)

    return fibre_group


def load_ks3_inner_array(pulse, instrument=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner lines of sight array.

    :param int pulse: JET pulse number.
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

    :param int pulse: JET pulse number.
    :param SpectroscopicInstrument instrument: One of the KS3 outer array instruments:
                                               array_polychromator, ksra and ksrb.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_array(pulse, 'outer', instrument=instrument, fibre_names=fibre_names, parent=parent)


def _load_ks3_single_los(pulse, los, instrument=None, parent=None):
    """
    Loads KS3 single line of sight.

    :param int pulse: JET pulse number.
    :param str los: KS3 line of sight: 'bunker', 'horizontal', 'horizontal limiter', 'vertical'.
    :param SpectroscopicInstrument instrument: One of the KS3 spectroscopic instruments.
    :param Node parent: The parent node in the scenegraph.
    """

    los = los.lower()
    if los not in ('bunker', 'horizontal', 'horizontal limiter', 'vertical'):
        raise ValueError("Line of sight {} is not supported."
                         " Choose between 'bunker', 'horizontal', 'horizontal limiter' and 'vertical'.".format(los))

    parameters = KS3_LOS_PARAMETERS[los]

    oldest_supported_pulse = min(parameters.keys())

    if pulse < oldest_supported_pulse:
        raise ValueError("Only shots >= {} are supported at this time.".format(oldest_supported_pulse))

    reference_pulse = reference_number(parameters, pulse)

    origin = parameters[reference_pulse]['origin']
    end = parameters[reference_pulse]['end']
    origin_radius = parameters[reference_pulse]['origin_radius']
    end_radius = parameters[reference_pulse]['end_radius']
    instruments = parameters[reference_pulse]['instruments']

    fibre_direction = origin.vector_to(end)
    acceptance_angle = np.rad2deg(np.arctan2(end_radius - origin_radius, fibre_direction.length))
    fibre_direction_norm = fibre_direction.normalise()
    fibre = SpectroscopicFibreOptic(origin, fibre_direction_norm, name='KS3 {} view'.format(los),
                                    acceptance_angle=acceptance_angle, radius=origin_radius, parent=parent)

    if instrument is None:

        return fibre

    if instrument not in instruments:
        intrument_names = ', '.join(instr.name for instr in instruments)
        raise ValueError("Only the following instruments are supported: {}.".format(intrument_names))

    fibre.connect_pipelines(instrument.pipeline_properties)

    (fibre.min_wavelength,
     fibre.max_wavelength,
     fibre.spectral_bins) = instrument.wavelength_settings(pulse)

    return fibre


def load_ks3_bunker(pulse, instrument=None, parent=None):
    """
    Loads KS3 bunker line of sight.

    :param int pulse: JET pulse number.
    :param SpectroscopicInstrument instrument: One of the KS3 bunker instruments:
                                               ksra or ksrb.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_single_los(pulse, 'bunker', instrument=instrument, parent=parent)


def load_ks3_horizontal(pulse, instrument=None, parent=None):
    """
    Loads KS3 horizontal line of sight.

    :param int pulse: JET pulse number.
    :param SpectroscopicInstrument instrument: global_polychromator or None.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_single_los(pulse, 'horizontal', instrument=instrument, parent=parent)


def load_ks3_horizontal_limiter(pulse, instrument=None, parent=None):
    """
    Loads KS3 horizontal limiter line of sight.

    :param int pulse: JET pulse number.
    :param SpectroscopicInstrument instrument: ksrb or None.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_single_los(pulse, 'horizontal limiter', instrument=instrument, parent=parent)


def load_ks3_vertical(pulse, instrument=None, parent=None):
    """
    Loads KS3 vertical line of sight.

    :param int pulse: JET pulse number.
    :param SpectroscopicInstrument instrument: global_polychromator or None.
    :param Node parent: The parent node in the scenegraph.
    """

    return _load_ks3_single_los(pulse, 'vertical', instrument=instrument, parent=parent)
