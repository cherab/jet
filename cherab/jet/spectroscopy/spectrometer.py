
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

import numpy as np

from jet.data import sal
from cherab.tools.spectroscopy import Spectrometer, CzernyTurnerSpectrometer
from .utility import reference_number


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
    :param int min_bins_per_pixel: Minimal number of spectral bins per pixel. Default is 1.
    :param str name: Spectrometer name.
    """

    def __init__(self, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters, pulse=None, min_bins_per_pixel=1, name=''):
        # initialising with mock-up values
        super().__init__(1, 1e-3, 1e7, 1e4, 10, ((500, 1),), min_bins_per_pixel=min_bins_per_pixel, name=name)
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

        wvl_path = '/pulse/{}/jpf/{}/{}-wave_in_req_sq_{}/data'.format(*jpf_tuple)
        reference_wavelength = 0.1 * sal.get(wvl_path).value  # A to nm

        pixtot_path = '/pulse/{}/jpf/{}/{}-campix_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixeltot = int(sal.get(pixtot_path).value)

        if 'reference_pixel' not in self._parameters[reference_pulse] or self._parameters[reference_pulse]['reference_pixel'] is None:
            reference_pixel = pixeltot // 2
        else:
            reference_pixel = self._parameters[reference_pulse]['reference_pixel']

        pixelon_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixelon = int(sal.get(pixelon_path).value)

        pixeloff_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixeloff = int(sal.get(pixeloff_path).value)

        pixel_spacing = self._parameters[reference_pulse]['pixel_spacing']

        if pixel_spacing < 0:
            # JET spectrometers can have negative resolution but Cherab spectrometers do not support this.
            reference_pixel = pixeltot - reference_pixel
            pixeloff = pixeltot - pixeloff - pixelon

        self._accommodated_spectra = None  # setting to None to avoid recalculating wavelength_to_pixel by property setters

        grating_path = '/pulse/{}/jpf/{}/{}-grate_in_req_sq_{}/data'.format(*jpf_tuple)
        self.grating = sal.get(grating_path).value * 1.e-6  # mm-1 to nm-1
        self.diffraction_order = self._parameters[reference_pulse]['diffraction_order']
        self.pixel_spacing = abs(pixel_spacing)
        self.diffraction_angle = self._parameters[reference_pulse]['diffraction_angle']
        self.focal_length = self._parameters[reference_pulse]['focal_length']

        min_wavelength = reference_wavelength
        for i in range(reference_pixel, pixeloff - 1, -1):
            min_wavelength = min_wavelength - self.resolution(min_wavelength)

        self.accommodated_spectra = ((min_wavelength, pixelon),)


class JetSurveySpectrometer(Spectrometer):
    """
    JET survey spectrometer.

    :param str jpf_subsystem: JPF subsystem, e.g. 'DD' for KS3.
    :param str jpf_node_prefix: Prefix of the JPF node, e.g. 'SR' for KS3.
    :param str jpf_node_sequence: Sequence of the JPF node, e.g. '002' for KSRB,
                                  '004' for KSRD.
    :param dict parameters: Spectrometer parameters are provided in the form
                            {jpn1: parameters1, jpn2: parameters2, ..., jpnN: parametersN},
                            where parameters1 are valid starting with the JET pulse number jpn1
                            till the pulse number jpn2 and parametersN are valid starting with
                            the pulse jpnN till now.

                            Each entry must contain the following parameter:
                            'disp_poly_coeff': List of the 4-th degree polynomial coefficients
                            in nm used to calculate pixel-to-wavelength calibration:
                            wavelength = c[0] + c[1] * pixel + c[2] * pixel**2 + ...
    :param int pulse: JET pulse number. Default is None.
    :param int min_bins_per_pixel: Minimal number of spectral bins
                                   per pixel. Default is 1.
    :param str name: Spectrometer name.
    """

    def __init__(self, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters, pulse=None,
                 min_bins_per_pixel=1, name=''):
        super().__init__(([500., 501.],), min_bins_per_pixel=min_bins_per_pixel, name=name)  # initialising with mock-up wavelength_to_pixel
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
        self.wavelength_to_pixel = (self.wavelength_to_pixel_from_jpf(value),)

    def wavelength_to_pixel_from_jpf(self, pulse):
        """
        Returns a wavelength-to-pixel calibration array based on the spectrometer settings
        for a given pulse.
        """

        reference_pulse = reference_number(self._parameters, pulse)
        coeff = self._parameters[reference_pulse]['disp_poly_coeff']

        jpf_tuple = (self._pulse, self._jpf_subsystem, self._jpf_node_prefix, self._jpf_node_sequence)
        pixelon_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixelon = int(sal.get(pixelon_path).value)

        pixeloff_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(*jpf_tuple)
        pixeloff = int(sal.get(pixeloff_path).value)

        pixels = np.arange(pixeloff, pixeloff + pixelon, pixelon, dtype=int)

        wavelength = coeff[0] + coeff[1] * pixels + coeff[2] * pixels**2 + coeff[3] * pixels**3 + coeff[4] * pixels**4

        disp = coeff[1] + 2 * coeff[1] * pixels + 3 * coeff[3] * pixels**2 + 4 * coeff[4] * pixels**3

        wavelength_to_pixel = np.empty(wavelength.size + 1)
        wavelength_to_pixel[0] = wavelength[0] - 0.5 * disp[0]
        wavelength_to_pixel[1:] = wavelength + 0.5 * disp

        if wavelength_to_pixel[-1] < wavelength_to_pixel[0]:
            # JET spectrometers can have negative resolution but Cherab spectrometers do not support this.
            wavelength_to_pixel = wavelength_to_pixel[::-1]

        return wavelength_to_pixel
