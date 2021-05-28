
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
from jet.data import sal
from raysect.optical.observer import SpectralRadiancePipeline0D

from .instrument import SpectroscopicInstrument
from .utility import reference_number
from .instrument_parameters import KS3_SURVEY_PARAMETERS, KS3_CZERNY_TURNER_PARAMETERS


class Spectrometer(SpectroscopicInstrument):
    """
    Spectrometer base class.

    :param str name: Spectrometer name.
    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_profix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '001' for KSRA,
                                  '002' for KSRB, '003' for KSRC, '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.
    """

    def __init__(self, name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters):
        super().__init__(name)
        self._jpf_subsystem = jpf_subsystem
        self._jpf_node_prefix = jpf_node_prefix
        self._jpf_node_sequence = jpf_node_sequence
        self._parameters = parameters
        self._oldest_supported_pulse = min(self._parameters.keys())
        self._pipeline_properties = [(SpectralRadiancePipeline0D, name, None)]

    def reference_wavelength(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-wave_in_req_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                        self._jpf_node_prefix, self._jpf_node_sequence)
        wavelength = sal.get(data_path).value

        return 0.1 * wavelength

    def pixel_off(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                          self._jpf_node_prefix, self._jpf_node_sequence)
        pixeloff = int(sal.get(data_path).value)

        return pixeloff

    def pixel_on(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                         self._jpf_node_prefix, self._jpf_node_sequence)
        pixelon = int(sal.get(data_path).value)

        return pixelon

    def pixel_total(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-campix_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                          self._jpf_node_prefix, self._jpf_node_sequence)
        pixeltotal = int(sal.get(data_path).value)

        return pixeltotal


class CzernyTurnerSpectrometer(Spectrometer):
    """
    Czerny-Turner high-resolution spectrometer.

    The perameters of spectrometer are provided in the form
    {jpn1: value1, jpn2: value2, ..., jpnN: valueN}, where value1
    is valid starting with the JET pulse number jpn1 till the pulse number jpn2
    and the valueN is valid starting with the pulse jpnN till now.

    :param str name: Spectrometer name.
    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_profix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.

                            Each entry must contain the following parameters:
                            'm': Diffraction order.
                            'focal_length': Focal length in nm.
                            'dxdp': Pixel to pixel spacing on CCD in nm.
                            'angle': Angle between incident and diffracted light in degrees.
                            'reference_pixel' (optional): The pixel number that corresponds
                            to the reference wavelength.
    """

    def resolution(self, pulse, wavelength):
        """
        Calculates spectral resolution in nm.

        :param int pulse: JET pulse number.
        :param float wavelength: Wavelength of the central pixel in nm.

        :return: resolution
        """

        data_path = '/pulse/{}/jpf/{}/{}-grate_in_req_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                         self._jpf_node_prefix, self._jpf_node_sequence)
        grating = sal.get(data_path).value * 1.e-6  # grating in nm-1

        reference_pulse = reference_number(self._parameters, pulse)

        m = self._parameters[reference_pulse]['m']
        dxdp = self._parameters[reference_pulse]['dxdp']
        angle = self._parameters[reference_pulse]['angle']
        fl = self._parameters[reference_pulse]['focal_length']

        p = 0.5 * m * grating * wavelength
        resolution = dxdp * (np.sqrt(np.cos(angle)**2 - p * p) - p * np.tan(angle)) / (m * fl * grating)

        return resolution

    def _set_wavelength(self, pulse):

        if pulse < self._oldest_supported_pulse:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(self._oldest_supported_pulse))

        pixel_total = self.pixel_total(pulse)

        reference_pulse = reference_number(self._parameters, pulse)

        if 'reference_pixel' not in self._parameters[reference_pulse] or self._parameters[reference_pulse]['reference_pixel'] is None:
            reference_pixel = pixel_total // 2
        else:
            reference_pixel = self._parameters[reference_pulse]['reference_pixel']

        reference_wavelength = self.reference_wavelength(pulse)
        pixeloff = self.pixel_off(pulse)
        pixelon = self.pixel_on(pulse)

        resolution = self.resolution(pulse, reference_wavelength)

        if resolution > 0:
            self._min_wavelength = (pixeloff - reference_pixel) * resolution + reference_wavelength
            self._max_wavelength = self._min_wavelength + pixelon * resolution
        else:
            self._min_wavelength = (pixeloff + pixelon - reference_pixel - 1) * resolution + reference_wavelength
            self._max_wavelength = self._min_wavelength - pixelon * resolution
        self._spectral_bins = pixelon
        self._pulse = pulse


class SurveySpectrometer(Spectrometer):
    """
    Survey spectrometer with a constant spectral resolution.

    Note: survey spectrometers usually have non-constant spectral resolution
    in the supported wavelength range. However, Raysect does not support
    the observers with variable spectral resolution.

    :param str name: Spectrometer name.
    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_profix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.

                            Each entry must contain the following parameters:
                            'resolution': Spectrometer resolution in nm.
                            'first_pixel_wavelength': Wavelength corresponding to the first pixel.
    """

    def _set_wavelength(self, pulse):

        if pulse < self._oldest_supported_pulse:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(self._oldest_supported_pulse))

        pixeloff = self.pixel_off(pulse)
        pixelon = self.pixel_on(pulse)
        pixeltotal = self.pixel_total(pulse)

        reference_pulse = reference_number(self._parameters, pulse)

        resolution = self._parameters[reference_pulse]['resolution']
        wavelength_0 = self._parameters[reference_pulse]['first_pixel_wavelength']

        if resolution > 0:
            self._min_wavelength = pixeloff * resolution + wavelength_0
            self._max_wavelength = self._min_wavelength + pixelon * resolution
        else:
            self._max_wavelength = wavelength_0 + (pixeloff + pixelon - pixeltotal) * resolution
            self._min_wavelength = self._max_wavelength + pixelon * resolution
        self._spectral_bins = pixelon
        self._pulse = pulse


ksra = SurveySpectrometer('ksra', 'dd', 'sr', '001', KS3_SURVEY_PARAMETERS['ksra'])

ksrb = CzernyTurnerSpectrometer('ksrb', 'dd', 'sr', '002', KS3_CZERNY_TURNER_PARAMETERS['ksrb'])

ksrc = SurveySpectrometer('ksrc', 'dd', 'sr', '003', KS3_SURVEY_PARAMETERS['ksrc'])

ksrd = CzernyTurnerSpectrometer('ksrd', 'dd', 'sr', '004', KS3_CZERNY_TURNER_PARAMETERS['ksrd'])
