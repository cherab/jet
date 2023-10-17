
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

from raysect.core import Point3D

from .instrument import array_polychromator, global_polychromator, ksra, ksrb, ksrc, ksrd


KS3_INNER_ARRAY_PARAMETERS = {
    80124: {
        'origin': [Point3D(-0.012, 3.3345, 3.58845) for i in range(10)],
        'end': [Point3D(-0.075, 2.228, -1.6),
                Point3D(-0.075, 2.273, -1.6),
                Point3D(-0.075, 2.315, -1.6),
                Point3D(-0.075, 2.363, -1.6),
                Point3D(-0.075, 2.409, -1.6),
                Point3D(-0.075, 2.453, -1.6),
                Point3D(-0.075, 2.498, -1.6),
                Point3D(-0.075, 2.542, -1.6),
                Point3D(-0.075, 2.586, -1.6),
                Point3D(-0.075, 2.631, -1.6)],
        'origin_radius': [0.0165 for i in range(10)],
        'end_radius': [0.0225 for i in range(10)],
        'instruments': (array_polychromator, ksrc, ksrd)
    },
    94115: {
        'origin': [Point3D(-0.012, 3.3345, 3.58845) for i in range(10)],
        'end': [Point3D(-0.075, 2.289, -1.6),
                Point3D(-0.075, 2.328, -1.6),
                Point3D(-0.075, 2.366, -1.6),
                Point3D(-0.075, 2.403, -1.6),
                Point3D(-0.075, 2.413, -1.6),
                Point3D(-0.075, 2.433, -1.6),
                Point3D(-0.075, 2.480, -1.6),
                Point3D(-0.075, 2.528, -1.6),
                Point3D(-0.075, 2.584, -1.6),
                Point3D(-0.075, 2.629, -1.6)],
        'origin_radius': [0.0165 for i in range(10)],
        'end_radius': [0.0225 for i in range(10)],
        'instruments': (array_polychromator, ksrc, ksrd)
    }
}

KS3_OUTER_ARRAY_PARAMETERS = {
    80124: {
        'origin': [Point3D(-0.012, 2.7733, 3.606) for i in range(10)],
        'end': [Point3D(-0.075, 2.521, -1.6),
                Point3D(-0.075, 2.567, -1.6),
                Point3D(-0.075, 2.611, -1.6),
                Point3D(-0.075, 2.654, -1.6),
                Point3D(-0.075, 2.697, -1.6),
                Point3D(-0.075, 2.744, -1.6),
                Point3D(-0.075, 2.787, -1.6),
                Point3D(-0.075, 2.830, -1.6),
                Point3D(-0.075, 2.886, -1.6),
                Point3D(-0.075, 2.955, -1.6)],
        'origin_radius': [0.0165 for i in range(10)],
        'end_radius': [0.0225 for i in range(10)],
        'instruments': (array_polychromator, ksra, ksrb)
    },
    94115: {
        'origin': [Point3D(-0.012, 2.7733, 3.606) for i in range(10)],
        'end': [Point3D(0.075, 2.619, -1.6),
                Point3D(0.075, 2.664, -1.6),
                Point3D(0.075, 2.702, -1.6),
                Point3D(0.075, 2.743, -1.6),
                Point3D(0.075, 2.786, -1.6),
                Point3D(0.075, 2.830, -1.6),
                Point3D(0.075, 2.874, -1.6),
                Point3D(0.075, 2.910, -1.6),
                Point3D(0.075, 2.962, -1.6),
                Point3D(0.075, 3.019, -1.6)],
        'origin_radius': [0.0165 for i in range(10)],
        'end_radius': [0.0225 for i in range(10)],
        'instruments': (array_polychromator, ksra, ksrb)
    }
}

KS3_BUNKER_PARAMETERS = {
    80124: {
        'origin': Point3D(9.98732, -17.49115, 0.000002),
        'end': Point3D(1.795, -0.27, 0),
        'origin_radius': 0.005,
        'end_radius': 0.06,
        'instruments': (ksra, ksrb)
    },
    92660: {
        'origin': Point3D(9.98732, -17.49115, 0.000002),
        'end': Point3D(1.795, -0.27, 0.027),
        'origin_radius': 0.005,
        'end_radius': 0.06,
        'instruments': (ksra, ksrb)
    }
}

KS3_HORIZONTAL_PARAMETERS = {
    80124: {
        'origin': Point3D(3.405942, 5.097291, 0.340673),
        'end': Point3D(1.060461, 1.414614, 0.108153),
        'origin_radius': 0.005,
        'end_radius': 0.05,
        'instruments': (global_polychromator,)
    }
}

KS3_HORIZONTAL_LIMITER_PARAMETERS = {
    80124: {
        'origin': Point3D(3.405942, 5.097291, 0.340673),
        'end': Point3D(0.984616, 1.47367, 0.196098),
        'origin_radius': 0.005,
        'end_radius': 0.05,
        'instruments': (ksrb,)
    }
}

KS3_VERTICAL_PARAMETERS = {
    80124: {
        'origin': Point3D(0.607699, 3.055148, 3.3543),
        'end': Point3D(0.672066, 3.181358, -1.2045),
        'origin_radius': 0.005,
        'end_radius': 0.0225,
        'instruments': (global_polychromator,)
    }
}


KS3_LOS_PARAMETERS = {
    'inner': KS3_INNER_ARRAY_PARAMETERS,
    'outer': KS3_OUTER_ARRAY_PARAMETERS,
    'bunker': KS3_BUNKER_PARAMETERS,
    'horizontal': KS3_HORIZONTAL_PARAMETERS,
    'horizontal limiter': KS3_HORIZONTAL_LIMITER_PARAMETERS,
    'vertical': KS3_VERTICAL_PARAMETERS
}
