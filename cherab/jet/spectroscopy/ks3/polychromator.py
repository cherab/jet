
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
from raysect.optical import InterpolatedSF
from raysect.optical.observer import RadiancePipeline0D

from .instrument import SpectroscopicInstrument


class PolychromatorFilter(InterpolatedSF):
    """
    Defines a symmetrical trapezoidal polychromator filter as a Raysect's InterpolatedSF.

    :param float wavelength: Central wavelength of the filter in nm.
    :param float window: Size of the filtering window in nm. Default is 3.
    :param float flat_top: Size of the flat top part of the filter in nm.
                           Default is None (equal to window).
    :param str name: Filter name (e.g. "H-alpha filter"). Default is ''.

    """

    def __init__(self, wavelength, window=3., flat_top=None, name=''):

        flat_top = flat_top or window - 1.e-15
        if flat_top > window:
            raise ValueError('flat_top must be less or equal than window.')
        if flat_top == window:
            flat_top = window - 1.e-15

        self.window = window
        self.flat_top = flat_top
        self.wavelength = wavelength
        self.name = name

        wavelengths = [wavelength - 0.5 * window,
                       wavelength - 0.5 * flat_top,
                       wavelength + 0.5 * flat_top,
                       wavelength + 0.5 * window]
        samples = [0, 1, 1, 0]
        super().__init__(wavelengths, samples, normalise=False)


d_alpha_filter = PolychromatorFilter(656.1, window=3., name='D alpha (PMT)')

baseline_523nm_filter = PolychromatorFilter(523, window=3., name='Bremsstrahlung 523 nm (PMT)')

be_ii_527nm_filter = PolychromatorFilter(527, window=3., name='Be II 527 nm (PMT)')

c_iii_465nm_filter = PolychromatorFilter(465, window=3., name='C III 465 nm (PMT)')

w_i_410nm_filter = PolychromatorFilter(410, window=3., name='W I 410 nm (PMT)')

he_i_668nm_filter = PolychromatorFilter(668, window=3., name='He I 668 nm (PMT)')

n_ii_567nm_filter = PolychromatorFilter(567, window=3., name='N II 567 nm (PMT)')


class Polychromator(SpectroscopicInstrument):
    """
    A polychromator assembly with a set of different filters.

    :param list filters: List of the PolychromatorFilter instances.
    :param int min_bins_per_window: Minimal number of spectral bins
                                    per filtering window. Default is 10.
    """

    def __init__(self, filters, min_bins_per_window=10):
        super().__init__()
        self._min_bins_per_window = min_bins_per_window
        self.filters = filters

    @property
    def min_bins_per_window(self):
        """
        Minimal number of spectral bins per filtering window. Default is 10.
        """
        return self._min_bins_per_window

    @min_bins_per_window.setter
    def min_bins_per_window(self, value):
        self._clear_wavelength_settings()
        self._min_bins_per_window = value

    @property
    def filters(self):
        """
        List of the PolychromatorFilter instances.
        """
        return self._filters

    @filters.setter
    def filters(self, value):
        self._clear_wavelength_settings()
        for poly_filter in value:
            if not isinstance(poly_filter, PolychromatorFilter):
                raise TypeError('Property filters must contain only PolychromatorFilter instances.')

        self._filters = value
        self._pipeline_properties = [(RadiancePipeline0D, poly_filter.name, poly_filter) for poly_filter in self._filters]

    def _set_wavelength(self, pulse):

        min_wavelength = np.inf
        max_wavelength = -np.inf
        step = np.inf
        for poly_filter in self.filters:
            step = min(step, poly_filter.window / self.min_bins_per_window)
            min_wavelength = min(min_wavelength, poly_filter.wavelength - 0.5 * poly_filter.window)
            max_wavelength = max(max_wavelength, poly_filter.wavelength + 0.5 * poly_filter.window)

        self._min_wavelength = min_wavelength
        self._max_wavelength = max_wavelength
        self._spectral_bins = int(np.ceil((max_wavelength - min_wavelength) / step))
        self._pulse = pulse


global_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                              c_iii_465nm_filter, w_i_410nm_filter, he_i_668nm_filter, n_ii_567nm_filter))

array_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                             c_iii_465nm_filter, w_i_410nm_filter))
