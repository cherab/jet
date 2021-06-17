
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
from cherab.jet.spectroscopy.utility import reference_number
from .sightline_parameters import KS3_LOS_PARAMETERS


def _load_ks3_array(pulse, array_type, instruments=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner or outer lines of sight array.

    :param int pulse: JET pulse number.
    :param str array_type: 'inner' or 'outer'.
    :param list instruments: The list of the KS3 inner or outer array instruments or None.
    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.

    :return FibreOpticGroup fibre_group: The KS3 sight line group.
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
    supported_instruments = parameters[reference_pulse]['instruments']

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

    if instruments is None or not len(instruments):

        return fibre_group

    min_wavelength = np.inf
    max_wavelength = 0
    bin_width = np.inf
    pipeline_properties = []
    for instrument in instruments:
        if instrument not in supported_instruments:
            intrument_names = ', '.join(instr.name for instr in supported_instruments)
            raise ValueError("Only the following instruments are supported: {}.".format(intrument_names))

        instrument.pulse = pulse  # does nothing if polychromator
        pipeline_properties += instrument.pipeline_properties
        min_wavelength = min(instrument.min_wavelength, min_wavelength)
        max_wavelength = max(instrument.max_wavelength, max_wavelength)
        bin_width = min((instrument.max_wavelength - instrument.min_wavelength) / instrument.spectral_bins, bin_width)

    fibre_group.connect_pipelines(pipeline_properties)
    fibre_group.min_wavelength = min_wavelength
    fibre_group.max_wavelength = max_wavelength
    fibre_group.spectral_bins = int(np.ceil((max_wavelength - min_wavelength) / bin_width))

    return fibre_group


def load_ks3_inner_array(pulse, instruments=None, fibre_names=None, parent=None):
    """
    Loads KS3 inner lines of sight array.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 inner array instruments or None.
                             The following instruments are supported: array_polychromator,
                             ksrc (survey spectrometer), ksrd (high-resolution spectrometer).

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the `FibreOpticGroup` default
                             settings are used.

    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.

    :return FibreOpticGroup fibre_group: The KS3 inner array sight lines.

    .. code-block:: pycon

        >>> ks3_inner_array = load_ks3_inner_array(90512, instruments=[array_polychromator, ksrc],
                                                   parent=world)
        >>> ks3_inner_array.pixel_samples = 5000
        >>> ks3_inner_array.spectral_bins = 2 * ks3_inner_array.spectral_bins
    """

    return _load_ks3_array(pulse, 'inner', instruments=instruments, fibre_names=fibre_names, parent=parent)


def load_ks3_outer_array(pulse, instruments=None, fibre_names=None, parent=None):
    """
    Loads KS3 outer lines of sight array.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 outer array instruments or None.
                             The following instruments are supported: array_polychromator,
                             ksra (survey spectrometer), ksrb (high-resolution spectrometer).

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the FibreOpticGroup default settings
                             are used.

    :param list fibre_names: The list of fibre names to load. E.g., ['1', '3', '5'] will load only
                             the 1st, 3rd and 5th sight lines.
    :param Node parent: The parent node in the scenegraph.

    :return FibreOpticGroup fibre_group: The KS3 outer array sight lines.

    .. code-block:: pycon

        >>> ks3_outer_array = load_ks3_inner_array(90512, instruments=[array_polychromator, ksra],
                                                   parent=world)
        >>> ks3_outer_array.pixel_samples = 5000
        >>> ks3_outer_array.spectral_bins = 2 * ks3_outer_array.spectral_bins
    """

    return _load_ks3_array(pulse, 'outer', instruments=instruments, fibre_names=fibre_names, parent=parent)


def _load_ks3_single_los(pulse, los, instruments=None, parent=None):
    """
    Loads KS3 single line of sight.

    :param int pulse: JET pulse number.
    :param str los: KS3 line of sight: 'bunker', 'horizontal', 'horizontal limiter', 'vertical'.
    :param list instruments: The list of the KS3 spectroscopic instruments.
    :param Node parent: The parent node in the scenegraph.

    :return SpectroscopicFibreOptic fibre: The KS3 single line of sight.
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
    supported_instruments = parameters[reference_pulse]['instruments']

    fibre_direction = origin.vector_to(end)
    acceptance_angle = np.rad2deg(np.arctan2(end_radius - origin_radius, fibre_direction.length))
    fibre_direction_norm = fibre_direction.normalise()
    fibre = SpectroscopicFibreOptic(origin, fibre_direction_norm, name='KS3 {} view'.format(los),
                                    acceptance_angle=acceptance_angle, radius=origin_radius, parent=parent)

    if instruments is None or not len(instruments):

        return fibre

    min_wavelength = np.inf
    max_wavelength = 0
    bin_width = np.inf
    pipeline_properties = []
    for instrument in instruments:
        if instrument not in supported_instruments:
            intrument_names = ', '.join(instr.name for instr in supported_instruments)
            raise ValueError("Only the following instruments are supported: {}.".format(intrument_names))

        instrument.pulse = pulse  # does nothing if polychromator
        pipeline_properties += instrument.pipeline_properties
        min_wavelength = min(instrument.min_wavelength, min_wavelength)
        max_wavelength = max(instrument.max_wavelength, max_wavelength)
        bin_width = min((instrument.max_wavelength - instrument.min_wavelength) / instrument.spectral_bins, bin_width)

    fibre.connect_pipelines(pipeline_properties)
    fibre.min_wavelength = min_wavelength
    fibre.max_wavelength = max_wavelength
    fibre.spectral_bins = int(np.ceil((max_wavelength - min_wavelength) / bin_width))

    return fibre


def load_ks3_bunker(pulse, instruments=None, parent=None):
    """
    Loads KS3 bunker line of sight.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 bunker line of sight instruments or None.
                             The following instruments are supported:
                             ksra (survey spectrometer), ksrb (high-resolution spectrometer).

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the SpectroscopicFibreOptic
                             default settings are used.

    :param Node parent: The parent node in the scenegraph.

    :return SpectroscopicFibreOptic fibre: The KS3 bunker line of sight.
    """

    return _load_ks3_single_los(pulse, 'bunker', instruments=instruments, parent=parent)


def load_ks3_horizontal(pulse, instruments=None, parent=None):
    """
    Loads KS3 horizontal line of sight.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 horizontal line of sight instruments or None.
                             The only instrument currently supported by this line of sight is
                             global_polychromator.

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the `SpectroscopicFibreOptic`
                             default settings are used.

    :param Node parent: The parent node in the scenegraph.

    :return SpectroscopicFibreOptic fibre: The KS3 horizontal line of sight.
    """

    return _load_ks3_single_los(pulse, 'horizontal', instruments=instruments, parent=parent)


def load_ks3_horizontal_limiter(pulse, instruments=None, parent=None):
    """
    Loads KS3 horizontal limiter line of sight.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 horizontal limiter line of sight instruments
                             or None. The only instrument currently supported by this line of
                             sight is ksrb.

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the `SpectroscopicFibreOptic`
                             default settings are used.

    :param Node parent: The parent node in the scenegraph.

    :return SpectroscopicFibreOptic fibre: The KS3 horizontal limiter line of sight.
    """

    return _load_ks3_single_los(pulse, 'horizontal limiter', instruments=instruments, parent=parent)


def load_ks3_vertical(pulse, instruments=None, parent=None):
    """
    Loads KS3 vertical line of sight.

    :param int pulse: JET pulse number.
    :param list instruments: The list of the KS3 horizontal limiter line of sight instruments
                             or None. The only instrument currently supported by this line of
                             sight is global_polychromator.

                             Caution! The settings of the instruments in the list will
                             be updated according to a given JET pulse number.

                             The instruments are used to add the appropriate pipelines
                             and set the following spectral properties of the observer:
                             `min_wavelength`, `max_wavelength`, `spectral_bins` according
                             to the actual instrument settings in a given JET pulse.

                             If multiple instruments are specified, the lower/upper limit of
                             the spectral range will be set to the lowest/highest limit of
                             all instruments, while the spectral resolution will be equal to the
                             highest value of all instruments. If needed, the user can override
                             the instrument settings, e.g. increase the number of
                             spectral bins.

                             If instruments are not specified, the `SpectroscopicFibreOptic`
                             default settings are used.

    :param Node parent: The parent node in the scenegraph.

    :return SpectroscopicFibreOptic fibre: The KS3 vertical line of sight.
    """

    return _load_ks3_single_los(pulse, 'vertical', instruments=instruments, parent=parent)
