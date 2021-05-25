
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

class SpectroscopicInstrument:
    """
    Base class for spectroscopic instruments (spectrometers, polychromators, etc.).
    This is an abstract class.
    """

    def __init__(self):
        self._clear_wavelength_settings()
        self._pipeline_properties = None

    @property
    def pipeline_properties(self):
        """
        The list of properties (class, name, filter) of the pipelines used with
        this instrument.
        """
        return self._pipeline_properties

    def wavelength_settings(self, pulse):
        """
        Returns the lower and upper wavelength bound and the number of spectral bins
        of this instrument.

        :param int pulse: JET pulse number.

        :return: (min_wavelength, max_wavelength, spectral_bins)
        """

        if not self._pulse or pulse != self._pulse:
            self._set_wavelength(pulse)

        return self._min_wavelength, self._max_wavelength, self._spectral_bins

    def _set_wavelength(self, pulse):
        raise NotImplementedError("To be defined in subclass.")

    def _clear_wavelength_settings(self):
        self._min_wavelength = None
        self._max_wavelength = None
        self._spectral_bins = None
        self._pulse = None
