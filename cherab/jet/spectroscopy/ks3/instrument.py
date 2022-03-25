
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

from cherab.tools.spectroscopy import TrapezoidalFilter, Polychromator
from cherab.jet.spectroscopy import JetCzernyTurnerSpectrometer, JetSurveySpectrometer


KS3_SURVEY_PARAMETERS = {
    'ksra': {
        80124: {
            'disp_poly_coeff': [417.309, 0.188978, 0.00000140778, 0, 0]
        },
        83901: {
            'disp_poly_coeff': [421.164, 0.1285, 0.00000098415, 0, 0]
        }
    },
    'ksrc': {
        80124: {
            'disp_poly_coeff': [570.298, -0.124456, -0.0000171539, 0, 0]
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


d_alpha_filter = TrapezoidalFilter(656.1, window=3., name='D alpha')

baseline_523nm_filter = TrapezoidalFilter(523, window=3., name='Bremsstrahlung 523 nm')

be_ii_527nm_filter = TrapezoidalFilter(527, window=3., name='Be II 527 nm')

c_iii_465nm_filter = TrapezoidalFilter(465, window=3., name='C III 465 nm')

w_i_410nm_filter = TrapezoidalFilter(410, window=3., name='W I 410 nm')

he_i_668nm_filter = TrapezoidalFilter(668, window=3., name='He I 668 nm')

n_ii_567nm_filter = TrapezoidalFilter(567, window=3., name='N II 567 nm')


global_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                              c_iii_465nm_filter, w_i_410nm_filter, he_i_668nm_filter,
                                              n_ii_567nm_filter), name='global_polychromator')

array_polychromator = Polychromator(filters=(d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter,
                                             c_iii_465nm_filter, w_i_410nm_filter), name='array_polychromator')


ksra = JetSurveySpectrometer('dd', 'sr', '001', KS3_SURVEY_PARAMETERS['ksra'], name='ksra')

ksrb = JetCzernyTurnerSpectrometer('dd', 'sr', '002', KS3_CZERNY_TURNER_PARAMETERS['ksrb'], name='ksrb')

ksrc = JetSurveySpectrometer('dd', 'sr', '003', KS3_SURVEY_PARAMETERS['ksrc'], name='ksrc')

ksrd = JetCzernyTurnerSpectrometer('dd', 'sr', '004', KS3_CZERNY_TURNER_PARAMETERS['ksrd'], name='ksrd')
