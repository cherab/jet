
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


class Spectrometer(SpectroscopicInstrument):
    """
    Spectrometer base class.

    :param str name: Spectrometer name.
    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_profix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '001' for KSRA,
                                  '002' for KSRB, '003' for KSRC, '004' for KSRD.
    """

    def __init__(self, name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence):
        super().__init__()
        self._jpf_subsystem = jpf_subsystem
        self._jpf_node_prefix = jpf_node_prefix
        self._jpf_node_sequence = jpf_node_sequence
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
    :param dict m: Diffraction order.
    :param dict focal_length: Focal length in nm.
    :param dict dxdp: Pixel to pixel spacing on CCD in nm.
    :param dict angle: Angle between incident and diffracted light in degrees.
    :param dict reference_pixel: The pixel number that corresponds to the reference wavelength.
                                 Default is None (central pixel).
    """

    def __init__(self, name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, m, focal_length, dxdp, angle, reference_pixel=None):
        super().__init__(name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence)
        self._m = m
        self._focal_length = focal_length
        self._dxdp = dxdp
        self._angle = angle
        self._reference_pixel = reference_pixel
        self._min_pulse = self._oldest_supported_pulse()

    def _oldest_supported_pulse(self):
        pulse_min_fl = min(self._focal_length.keys())
        pulse_min_m = min(self._m.keys())
        pulse_min_dxdp = min(self._dxdp.keys())
        pulse_min_angle = min(self._angle.keys())
        pulse_min_rp = 0 if self._reference_pixel is None else min(self._reference_pixel.keys())

        return max(pulse_min_fl, pulse_min_m, pulse_min_dxdp, pulse_min_angle, pulse_min_rp)

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

        m = self._m[reference_number(self._m, pulse)]
        dxdp = self._dxdp[reference_number(self._dxdp, pulse)]
        angle = np.deg2rad(self._angle[reference_number(self._angle, pulse)])
        fl = self._focal_length[reference_number(self._focal_length, pulse)]

        p = 0.5 * m * grating * wavelength
        resolution = dxdp * (np.sqrt(np.cos(angle)**2 - p * p) - p * np.tan(angle)) / (m * fl * grating)

        return resolution

    def _set_wavelength(self, pulse):

        if pulse < self._min_pulse:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(self._min_pulse))

        pixel_total = self.pixel_total(pulse)

        if self._reference_pixel is None:
            reference_pixel = pixel_total // 2
        else:
            reference_pixel = self._reference_pixel[reference_number(self._reference_pixel, pulse)] or pixel_total // 2

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

    The perameters of spectrometer are provided in the form
    {jpn1: value1, jpn2: value2, ..., jpnN: valueN}, where value1
    is valid starting with the JET pulse number jpn1 till the pulse number jpn2
    and the valueN is valid starting with the pulse jpnN till now.

    :param str name: Spectrometer name.
    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_profix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict resolution: Spectrometer resolution in nm.
    :param dict wavelength_0: Wavelength corresponding to the first pixel.
    """
    def __init__(self, name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, resolution, wavelength_0):
        super().__init__(name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence)
        self._resolution = resolution
        self._wavelength_0 = wavelength_0
        self._min_pulse = self._oldest_supported_pulse()

    def _oldest_supported_pulse(self):
        pulse_min_res = min(self._resolution.keys())
        pulse_min_wl = min(self._wavelength_0.keys())

        return max(pulse_min_res, pulse_min_wl)

    def _set_wavelength(self, pulse):

        if pulse < self._min_pulse:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(self._min_pulse))

        pixeloff = self.pixel_off(pulse)
        pixelon = self.pixel_on(pulse)
        pixeltotal = self.pixel_total(pulse)

        resolution = self._resolution[reference_number(self._resolution, pulse)]
        wavelength_0 = self._wavelength_0[reference_number(self._wavelength_0, pulse)]

        if resolution > 0:
            self._min_wavelength = pixeloff * resolution + wavelength_0
            self._max_wavelength = self._min_wavelength + pixelon * resolution
        else:
            self._max_wavelength = wavelength_0 + (pixeloff + pixelon - pixeltotal) * resolution
            self._min_wavelength = self._max_wavelength + pixelon * resolution
        self._spectral_bins = pixelon
        self._pulse = pulse


ksra = SurveySpectrometer('ksra', 'dd', 'sr', '001', resolution={80124: 0.19042, 83901: 0.12951},
                          wavelength_0={80124: 417.2448, 83901: 421.0998})

ksrb = CzernyTurnerSpectrometer('ksrb', 'dd', 'sr', '002', m={80124: 1}, focal_length={80124: 0.999596e9, 85501: 0.99876298e9},
                                dxdp={80124: 0.0225e6, 85501: 0.013e6}, angle={80124: 7.176090, 85501: 7.1812114},
                                reference_pixel={80124: 362, 85501: 522})

ksrc = SurveySpectrometer('ksrc', 'dd', 'sr', '003', resolution={80124: -0.14202}, wavelength_0={80124: 570.36})

ksrd = CzernyTurnerSpectrometer('ksrd', 'dd', 'sr', '004', m={80124: 1}, focal_length={80124: 0.99706828e9},
                                dxdp={80124: -0.013e6}, angle={80124: 7.2210486},
                                reference_pixel=None)
