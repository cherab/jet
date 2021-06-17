
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

from raysect.optical.observer import SpectralRadiancePipeline0D
from cherab.tools.observers.spectroscopy import SurveySpectrometer, CzernyTurnerSpectrometer
from sal.client import SALClient  # this also works outside JET cluster, where jet.data is not available

from .utility import reference_number


sal = SALClient('https://sal.jet.uk')


class JetCzernyTurnerSpectrometer(CzernyTurnerSpectrometer):
    """
    JET Czerny-Turner high-resolution spectrometer.

    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_prefix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.

                            Each entry must contain the following parameters:
                            'diffraction_order': Diffraction order.
                            'focal_length': Focal length in nm.
                            'pixel_spacing': Pixel to pixel spacing on CCD in nm.
                            'diffraction_angle': Angle between incident and diffracted light in degrees.
                            'reference_pixel' (optional): The pixel number that corresponds
                            to the reference wavelength.
    :param int pulse: JET pulse number. Default is None (oldest supported pulse).
    :param str name: Spectrometer name.
    """

    def __init__(self, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters, pulse=None, name=''):
        super().__init__(1, 1e-3, 1e7, 1e4, 10, 100, 500, None, name)  # initialising with mock values
        self._jpf_subsystem = jpf_subsystem
        self._jpf_node_prefix = jpf_node_prefix
        self._jpf_node_sequence = jpf_node_sequence
        self._parameters = parameters
        self._oldest_supported_pulse = min(self._parameters.keys())
        self._pulse = None
        self.pulse = pulse or self._oldest_supported_pulse

    @property
    def pulse(self):
        """ JET pulse number."""
        return self._pulse

    @pulse.setter
    def pulse(self, value):

        if self._pulse and self._pulse == value:
            return

        value = int(value)
        if value < self._oldest_supported_pulse:
            raise ValueError("Only pulses >= {} are supported for this spectrometer.".format(self._oldest_supported_pulse))

        self._pulse = value
        self._update_parameters()

    def _update_parameters(self):

        reference_pulse = reference_number(self._parameters, self._pulse)

        jpf_tuple = (self._pulse, self._jpf_subsystem, self._jpf_node_prefix, self._jpf_node_sequence)

        grating_path = '/pulse/{}/jpf/{}/{}-grate_in_req_sq_{}/data'.format(*jpf_tuple)
        self.grating = sal.get(grating_path).value * 1.e-6  # mm-1 to nm-1

        wvl_path = '/pulse/{}/jpf/{}/{}-wave_in_req_sq_{}/data'.format(*jpf_tuple)
        self.reference_wavelength = 0.1 * sal.get(wvl_path).value  # A to nm

        self.diffraction_order = self._parameters[reference_pulse]['diffraction_order']
        self.pixel_spacing = self._parameters[reference_pulse]['pixel_spacing']
        self.diffraction_angle = self._parameters[reference_pulse]['diffraction_angle']
        self.focal_length = self._parameters[reference_pulse]['focal_length']

        if 'reference_pixel' not in self._parameters[reference_pulse] or self._parameters[reference_pulse]['reference_pixel'] is None:
            pixtot_path = '/pulse/{}/jpf/{}/{}-campix_in_mpx_sq_{}/data'.format(*jpf_tuple)
            pixel_total = int(sal.get(pixtot_path).value)
            reference_pixel = pixel_total // 2
        else:
            reference_pixel = self._parameters[reference_pulse]['reference_pixel']

        pixelon_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(*jpf_tuple)
        self.spectral_bins = int(sal.get(pixelon_path).value)

        pixeloff_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixeloff = int(sal.get(pixeloff_path).value)

        self.reference_bin = reference_pixel - pixeloff

        self._clear_spectral_settings()


class JetSurveySpectrometer(SurveySpectrometer):
    """
    JET survey spectrometer with a constant spectral resolution.

    Note: survey spectrometers usually have non-constant spectral resolution
    in the supported wavelength range. However, Raysect does not support
    the observers with variable spectral resolution.

    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_prefix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.

                            Each entry must contain the following parameters:
                            'resolution': Spectrometer resolution in nm.
                            'reference_wavelength': Wavelength corresponding to the reference pixel.
                            'reference_pixel': Reference CCD pixel index.
    :param int pulse: JET pulse number. Default is None.
    :param str name: Spectrometer name.
    """

    def __init__(self, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters, pulse=None, name=''):
        super().__init__(1., 1, 500., 0, name)  # initialising with mock values
        self._jpf_subsystem = jpf_subsystem
        self._jpf_node_prefix = jpf_node_prefix
        self._jpf_node_sequence = jpf_node_sequence
        self._parameters = parameters
        self._oldest_supported_pulse = min(self._parameters.keys())
        self._pulse = None
        self.pulse = pulse or self._oldest_supported_pulse

    @property
    def pulse(self):
        """ JET pulse number."""
        return self._pulse

    @pulse.setter
    def pulse(self, value):

        if self._pulse and self._pulse == value:
            return

        value = int(value)
        if value < self._oldest_supported_pulse:
            raise ValueError("Only pulses >= {} are supported for this spectrometer.".format(self._oldest_supported_pulse))

        self._pulse = value
        self._update_parameters()

    def _update_parameters(self):

        reference_pulse = reference_number(self._parameters, self._pulse)
        self.resolution = self._parameters[reference_pulse]['resolution']
        self.reference_wavelength = self._parameters[reference_pulse]['reference_wavelength']
        reference_pixel = self._parameters[reference_pulse]['reference_pixel']

        jpf_tuple = (self._pulse, self._jpf_subsystem, self._jpf_node_prefix, self._jpf_node_sequence)
        pixelon_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(*jpf_tuple)
        self.spectral_bins = int(sal.get(pixelon_path).value)

        pixeloff_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixeloff = int(sal.get(pixeloff_path).value)

        self.reference_bin = reference_pixel - pixeloff

        self._clear_spectral_settings()
