
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


KS3_SURVEY_PARAMETERS = {
    'ksra': {
        80124: {
            'resolution': 0.19042,
            'first_pixel_wavelength': 417.2448
        },
        83901: {
            'resolution': 0.12951,
            'first_pixel_wavelength': 421.0998
        }
    },
    'ksrc': {
        80124: {
            'resolution': -0.14202,
            'first_pixel_wavelength': 570.36
        }
    }
}

KS3_CZERNY_TURNER_PARAMETERS = {
    'ksrb': {
        80124: {
            'm': 1,
            'dxdp': 0.0225e6,
            'focal_length': 0.999596e9,
            'angle': 7.176090,
            'reference_pixel': 362
        },
        85501: {
            'm': 1,
            'dxdp': 0.013e6,
            'focal_length': 0.99876298e9,
            'angle': 7.1812114,
            'reference_pixel': 522
        }
    },
    'ksrd': {
        80124: {
            'm': 1,
            'dxdp': -0.013e6,
            'focal_length': 0.99706828e9,
            'angle': 7.2210486
        }
    }
}
