
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

from cherab.tools.observers.spectroscopy import PolychromatorFilter, Polychromator
from cherab.jet.spectroscopy import JetCzernyTurnerSpectrometer, JetSurveySpectrometer


KS3_SURVEY_PARAMETERS = {
    'ksra': {
        80124: {
            'resolution': 0.1904294,
            'reference_wavelength': 419.3879,
            'reference_pixel': 10
        },
        83901: {
            'resolution': 0.1295087,
            'reference_wavelength': 421.2925,
            'reference_pixel': 0
        }
    },
    'ksrc': {
        80124: {
            'resolution': -0.1420387,
            'reference_wavelength': 570.1735,
            'reference_pixel': 0
        }
    }
}

KS3_CZERNY_TURNER_PARAMETERS = {
    'ksrb': {
        80124: {
            'diffraction_order': 1,
            'pixel_spacing': 2.25e4,
            'focal_length': 0.999596e9,
            'diffraction_angle': 7.176090,
            'reference_pixel': None
        },
        85501: {
            'diffraction_order': 1,
            'pixel_spacing': 1.3e4,
            'focal_length': 0.99876298e9,
            'diffraction_angle': 7.1812114,
            'reference_pixel': None
        }
    },
    'ksrd': {
        80124: {
            'diffraction_order': 1,
            'pixel_spacing': -1.3e4,
            'focal_length': 0.99706828e9,
            'diffraction_angle': 7.2210486,
            'reference_pixel': None
        }
    }
}


d_alpha_filter = PolychromatorFilter(656.1, window=3., name='D alpha')

baseline_523nm_filter = PolychromatorFilter(523, window=3., name='Bremsstrahlung 523 nm')

be_ii_527nm_filter = PolychromatorFilter(527, window=3., name='Be II 527 nm')

c_iii_465nm_filter = PolychromatorFilter(465, window=3., name='C III 465 nm')

w_i_410nm_filter = PolychromatorFilter(410, window=3., name='W I 410 nm')

he_i_668nm_filter = PolychromatorFilter(668, window=3., name='He I 668 nm')

n_ii_567nm_filter = PolychromatorFilter(567, window=3., name='N II 567 nm')


global_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                              c_iii_465nm_filter, w_i_410nm_filter, he_i_668nm_filter,
                                              n_ii_567nm_filter), name='global_polychromator')

array_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                             c_iii_465nm_filter, w_i_410nm_filter), name='array_polychromator')


ksra = JetSurveySpectrometer('dd', 'sr', '001', KS3_SURVEY_PARAMETERS['ksra'], name='ksra')

ksrb = JetCzernyTurnerSpectrometer('dd', 'sr', '002', KS3_CZERNY_TURNER_PARAMETERS['ksrb'], name='ksrb')

ksrc = JetSurveySpectrometer('dd', 'sr', '003', KS3_SURVEY_PARAMETERS['ksrc'], name='ksrc')

ksrd = JetCzernyTurnerSpectrometer('dd', 'sr', '004', KS3_CZERNY_TURNER_PARAMETERS['ksrd'], name='ksrd')
