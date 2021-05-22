import numpy as np
from jet.data import sal
from raysect.optical.observer import SpectralRadiancePipeline0D

from .instrument import SpectroscopicInstrument


class Spectrometer(SpectroscopicInstrument):

    def __init__(self, name, jpf_subsystem, jpf_node_prefix, jpf_node_sequence, parameters):
        super().__init__()
        self._jpf_subsystem = jpf_subsystem
        self._jpf_node_prefix = jpf_node_prefix
        self._jpf_node_sequence = jpf_node_sequence
        self._parameters = parameters
        self._pipeline_properties = [(SpectralRadiancePipeline0D, name, None)]

    def _reference_pixel(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-campix_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                          self._jpf_node_prefix, self._jpf_node_sequence)
        campixel = int(sal.get(data_path).value)

        return campixel // 2

    def _reference_wavelength(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-wave_in_req_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                        self._jpf_node_prefix, self._jpf_node_sequence)
        wavelength = sal.get(data_path).value

        return 0.1 * wavelength

    def _pixel_off(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-pixoff_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                          self._jpf_node_prefix, self._jpf_node_sequence)
        pixeloff = int(sal.get(data_path).value)

        return pixeloff

    def _pixel_on(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-pixon_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                         self._jpf_node_prefix, self._jpf_node_sequence)
        pixelon = int(sal.get(data_path).value)

        return pixelon

    def _pixel_total(self, pulse):

        data_path = '/pulse/{}/jpf/{}/{}-campix_in_mpx_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                          self._jpf_node_prefix, self._jpf_node_sequence)
        pixeltotal = int(sal.get(data_path).value)

        return pixeltotal

class HighResSpectrometer(Spectrometer):

    def _resolution(self, pulse, reference_wavelength, reference_pulse):

        data_path = '/pulse/{}/jpf/{}/{}-grate_in_req_sq_{}/data'.format(pulse, self._jpf_subsystem,
                                                                         self._jpf_node_prefix, self._jpf_node_sequence)
        grating = sal.get(data_path).value * 1.e-7

        mm = self._parameters[reference_pulse]['mm']
        dxdp = self._parameters[reference_pulse]['dxdp'] * 1.e6
        fl = self._parameters[reference_pulse]['fl'] * 1.e10
        angle = self._parameters[reference_pulse]['angle'] * np.pi / 180.
        p = 5. * mm * grating * reference_wavelength
        resolution = dxdp * (np.sqrt(np.cos(angle)**2 - p * p) - p * np.tan(angle)) / (mm * fl * grating)

        return resolution

    def _set_wavelength(self, pulse):

        pulse_min = min(self._parameters.keys())
        if pulse < pulse_min:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(pulse_min))

        keys = sorted(self._parameters.keys(), reverse=True)
        for key in keys:
            if pulse >= key:
                reference_pulse = key
                break

        reference_pixel = self._parameters[reference_pulse]['reference_pixel'] or self._reference_pixel(pulse)
        reference_wavelength = self._reference_wavelength(pulse)
        pixeloff = self._pixel_off(pulse)
        pixelon = self._pixel_on(pulse)

        resolution = self._resolution(pulse, reference_wavelength, reference_pulse)

        if resolution > 0:
            self._min_wavelength = (pixeloff - reference_pixel) * resolution + reference_wavelength
            self._max_wavelength = self._min_wavelength + pixelon * resolution
        else:
            self._min_wavelength = (pixeloff + pixelon - reference_pixel - 1) * resolution + reference_wavelength
            self._max_wavelength = self._min_wavelength - pixelon * resolution
        self._spectral_bins = pixelon
        self._pulse = pulse


class SurveySpectrometer(Spectrometer):

    def _set_wavelength(self, pulse):

        pulse_min = min(self._parameters.keys())
        if pulse < pulse_min:
            raise ValueError("Only shots >= {} are supported for this spectrometer.".format(pulse_min))

        keys = sorted(self._parameters.keys(), reverse=True)
        for key in keys:
            if pulse >= key:
                reference_pulse = key
                break

        pixeloff = self._pixel_off(pulse)
        pixelon = self._pixel_on(pulse)
        pixeltotal = self._pixel_total(pulse)

        resolution = self._parameters[reference_pulse]['resolution']
        wavelength_0 = self._parameters[reference_pulse]['wavelength_0']

        if resolution > 0:
            self._min_wavelength = pixeloff * resolution + wavelength_0
            self._max_wavelength = self._min_wavelength + pixelon * resolution
        else:
            self._max_wavelength = wavelength_0 + (pixeloff + pixelon - pixeltotal) * resolution
            self._min_wavelength = self._max_wavelength + pixelon * resolution
        self._spectral_bins = pixelon
        self._pulse = pulse


ksra = SurveySpectrometer('ksra', 'DD', 'SR', '001', {80124: {'resolution': 0.19042, 'wavelength_0': 417.2448},
                                                      83901: {'resolution': 0.12951, 'wavelength_0': 421.0998}})

ksrb = HighResSpectrometer('ksrb', 'DD', 'SR', '002', {85501: {'mm': 1., 'fl': 0.99876298, 'dxdp': 0.013, 'angle': 7.1812114, 'reference_pixel': 522},
                                                       80124: {'mm': 1., 'fl': 0.999596, 'dxdp': 0.0225, 'angle': 7.176090, 'reference_pixel': 362}})

ksrc = SurveySpectrometer('ksrc', 'DD', 'SR', '003', {80124: {'resolution': -0.14202, 'wavelength_0': 570.36}})

ksrd = HighResSpectrometer('ksrd', 'DD', 'SR', '004', {80124: {'mm': 1., 'fl': 0.99706828, 'dxdp': -0.013, 'angle': 7.2210486, 'reference_pixel': None}})
