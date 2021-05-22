
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

    def __init__(self, central_wavelength, window=3., plateau=None, name='', normalise=False):

        plateau = plateau or window - 1.e-15
        if plateau > window:
            raise ValueError('Plateau must be less or equal than window.')
        if plateau == window:
            plateau = window - 1.e-15

        self.window = window
        self.plateau = plateau
        self.central_wavelength = central_wavelength
        self.name = name

        wavelengths = [central_wavelength - 0.5 * window,
                       central_wavelength - 0.5 * plateau,
                       central_wavelength + 0.5 * plateau,
                       central_wavelength + 0.5 * window]
        samples = [0, 1, 1, 0]
        super().__init__(wavelengths, samples, normalise=normalise)


d_alpha_filter = PolychromatorFilter(656.1, window=3., name='D alpha (PMT)')

baseline_523nm_filter = PolychromatorFilter(523, window=3., name='Bremsstrahlung 523 nm (PMT)')

be_ii_527nm_filter = PolychromatorFilter(527, window=3., name='Be II 527 nm (PMT)')

c_iii_465nm_filter = PolychromatorFilter(465, window=3., name='C III 465 nm (PMT)')

w_i_410nm_filter = PolychromatorFilter(410, window=3., name='W I 410 nm (PMT)')

he_i_668nm_filter = PolychromatorFilter(668, window=3., name='He I 668 nm (PMT)')

n_ii_567nm_filter = PolychromatorFilter(567, window=3., name='N II 567 nm (PMT)')


class Polychromator(SpectroscopicInstrument):

    def __init__(self, filters, min_bins_per_window=10):
        super().__init__()
        self._min_bins_per_window = min_bins_per_window
        self.filters = filters

    @property
    def min_bins_per_window(self):
        return self._min_bins_per_window

    @min_bins_per_window.setter
    def min_bins_per_window(self, value):
        self._clear_wavelength_settings()
        self._min_bins_per_window = value

    @property
    def filters(self):
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
            min_wavelength = min(min_wavelength, poly_filter.central_wavelength - 0.5 * poly_filter.window)
            max_wavelength = max(max_wavelength, poly_filter.central_wavelength + 0.5 * poly_filter.window)

        self._min_wavelength = min_wavelength
        self._max_wavelength = max_wavelength
        self._spectral_bins = int(np.ceil((max_wavelength - min_wavelength) / step))
        self._pulse = pulse


global_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                              c_iii_465nm_filter, w_i_410nm_filter, he_i_668nm_filter, n_ii_567nm_filter))

array_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                             c_iii_465nm_filter, w_i_410nm_filter))
