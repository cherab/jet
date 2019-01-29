
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

"""
JET equilibrium data reading routines
"""

import numpy as np

from raysect.core import Point2D
from cherab.tools.equilibrium import EFITEquilibrium

from jet.data import sal
from sal.core.exception import NodeNotFound


# special JET constant that signifies if an x-point is not present
X_POINT_UNAVAILABLE = -10


class JETEquilibrium:
    """
    Reads JET EFIT equilibrium data and provides object access to each timeslice.

    :param pulse: Jet pulse number.
    :param user: PPF user ID (default: jetppf).
    :param dda: PPF DDA name (default: efit).
    :param sequence: PPF sequence number (default: 0).
    """

    def __init__(self, pulse, user=None, dda=None, sequence=None):

        DDA_PATH = '/pulse/{}/ppf/signal/{}/{}:{}'
        DATA_PATH = '/pulse/{}/ppf/signal/{}/{}/{}:{}'

        # defaults
        user = user or 'jetppf'
        dda = dda or 'efit'
        sequence = sequence or 0

        self.pulse = pulse
        self.user = user
        self.dda = dda

        # identify the current head sequence number if seq = 0 to ensure all data from same sequence
        # this should mitigate the very low probability event of new data being written part way through the read
        if sequence == 0:
            r = sal.list(DDA_PATH.format(pulse, user, dda, sequence))
            sequence = r.revision_latest
        self.sequence = sequence

        # obtain psi data and timebase
        self._packed_psi = sal.get(DATA_PATH.format(pulse, user, dda, 'psi', sequence))
        self.time_slices = self._packed_psi.dimensions[0].data

        # psi grid axis
        self._r = sal.get(DATA_PATH.format(pulse, user, dda, 'psir', sequence)).data
        self._z = sal.get(DATA_PATH.format(pulse, user, dda, 'psiz', sequence)).data

        # obtain f-profile
        self._f = sal.get(DATA_PATH.format(pulse, user, dda, 'f', sequence))

        # q profile
        self._q = sal.get(DATA_PATH.format(pulse, user, dda, 'q', sequence))

        # obtain psi at the plasma boundary and magnetic axis
        self._psi_lcfs = sal.get(DATA_PATH.format(pulse, user, dda, 'fbnd', sequence))
        self._psi_axis = sal.get(DATA_PATH.format(pulse, user, dda, 'faxs', sequence))

        # obtain magnetic axis coordinates
        self._axis_coord_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rmag', sequence))
        self._axis_coord_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zmag', sequence))

        # obtain x-points
        self._lower_xpoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rxpl', sequence))
        self._lower_xpoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zxpl', sequence))

        self._upper_xpoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rxpu', sequence))
        self._upper_xpoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zxpu', sequence))

        # obtain strike-points
        self._lower_inner_strikepoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rsil', sequence))
        self._lower_inner_strikepoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zsil', sequence))

        self._lower_outer_strikepoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rsol', sequence))
        self._lower_outer_strikepoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zsol', sequence))

        self._upper_inner_strikepoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rsiu', sequence))
        self._upper_inner_strikepoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zsiu', sequence))

        self._upper_outer_strikepoint_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rsou', sequence))
        self._upper_outer_strikepoint_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zsou', sequence))

        # obtain vacuum magnetic field sample
        self._b_vacuum_magnitude = sal.get(DATA_PATH.format(pulse, user, dda, 'bvac', sequence))

        # obtain lcfs boundary polygon
        self._lcfs_poly_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rbnd', sequence))
        self._lcfs_poly_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zbnd', sequence))

        # obtain limiter polygon
        try:
            self._limiter_poly_r = sal.get(DATA_PATH.format(pulse, user, dda, 'rlim', sequence))
            self._limiter_poly_z = sal.get(DATA_PATH.format(pulse, user, dda, 'zlim', sequence))
        except NodeNotFound:
            self._limiter_poly_r = None
            self._limiter_poly_z = None

        self.time_range = self.time_slices.min(), self.time_slices.max()

    def __call__(self, time):
        self.time(self, time)

    def time(self, time):
        """
        Returns an equilibrium object for the time-slice closest to the requested time.

        The specific time-slice returned is held in the time attribute of the returned object.

        :param time: The equilibrium time point.
        :returns: An EFITEquilibrium object.
        """

        B_VACUUM_RADIUS = 2.96  # meters

        # locate the nearest time point and fail early if we are outside the time range of the data
        try:
            index = self._find_nearest(self.time_slices, time)
        except IndexError:
            raise ValueError('Requested time lies outside the range of the data: [{}, {}]s.'.format(*self.time_range))

        # slice data for selected time point
        time = self.time_slices[index]
        psi_lcfs = self._psi_lcfs.data[index]
        psi_axis = self._psi_axis.data[index]
        axis_coord = Point2D(self._axis_coord_r.data[index], self._axis_coord_z.data[index])
        b_vacuum_magnitude = self._b_vacuum_magnitude.data[index]
        x_points, strike_points = self._process_points(index)

        # pack f_profile into a Nx2 array
        f_profile = np.zeros((2, self._f.dimensions[1].length))
        f_profile[0, :] = self._f.dimensions[1].data
        f_profile[1, :] = self._f.data[index, :]

        # pack q_profile into a Nx2 array
        q_profile = np.zeros((2, self._q.dimensions[1].length))
        q_profile[0, :] = self._q.dimensions[1].data
        q_profile[1, :] = self._q.data[index, :]

        # slice and reshape psi data for specified time point
        # the original data is 3D, packed into a 2D array, this must be reshaped
        psi = np.reshape(self._packed_psi.data[index, :], (len(self._r.data), len(self._z.data)), order='F')

        # convert raw poly coordinates into a polygon
        lcfs_poly_r = self._lcfs_poly_r.data[index, :]
        lcfs_poly_z = self._lcfs_poly_z.data[index, :]
        lcfs_polygon = self._process_efit_polygon(lcfs_poly_r, lcfs_poly_z)

        if self._limiter_poly_r and self._limiter_poly_z:
            # todo: when efit reprocessed this data will be 1D, working around a bug in idl efit->ppf code.
            limiter_polygon = self._process_efit_polygon(self._limiter_poly_r.data[0, :], self._limiter_poly_z.data[0, :])
        else:
            limiter_polygon = None

        return EFITEquilibrium(self._r, self._z, psi, psi_axis, psi_lcfs, axis_coord, x_points, strike_points,
                               f_profile, q_profile, B_VACUUM_RADIUS, b_vacuum_magnitude,
                               lcfs_polygon, limiter_polygon, time)

    @staticmethod
    def _find_nearest(array, value):

        if value < array.min() or value > array.max():
            raise IndexError("Requested value is outside the range of the data.")

        index = np.searchsorted(array, value, side="left")

        if (value - array[index])**2 < (value - array[index + 1])**2:
            return index
        else:
            return index + 1

    def _process_points(self, index):

        x_points = []
        strike_points = []

        # is lower x-point present?
        lower = Point2D(self._lower_xpoint_r.data[index], self._lower_xpoint_z.data[index])
        if not (lower.x == X_POINT_UNAVAILABLE and lower.y == X_POINT_UNAVAILABLE):
            x_points.append(lower)
            strike_points += [
                Point2D(self._lower_inner_strikepoint_r.data[index], self._lower_inner_strikepoint_z.data[index]),
                Point2D(self._lower_outer_strikepoint_r.data[index], self._lower_outer_strikepoint_z.data[index])
            ]

        # is upper x-point present?
        upper = Point2D(self._upper_xpoint_r.data[index], self._upper_xpoint_z.data[index])
        if not (upper.x == X_POINT_UNAVAILABLE and upper.y == X_POINT_UNAVAILABLE):
            x_points.append(upper)
            strike_points += [
                Point2D(self._upper_inner_strikepoint_r.data[index], self._upper_inner_strikepoint_z.data[index]),
                Point2D(self._upper_outer_strikepoint_r.data[index], self._upper_outer_strikepoint_z.data[index])
            ]

        return x_points, strike_points

    @staticmethod
    def _process_efit_polygon(poly_r, poly_z):

        if poly_r.shape != poly_z.shape:
            raise ValueError("EFIT polygon coordinate arrays are inconsistent in length.")

        n = poly_r.shape[0]
        if n < 2:
            raise ValueError("EFIT polygon coordinate contain less than 2 points.")

        # boundary polygon contains redundant points that must be removed
        unique = (poly_r != poly_r[0]) | (poly_z != poly_z[0])
        unique[0] = True  # first point must be included!
        poly_r = poly_r[unique]
        poly_z = poly_z[unique]

        # generate single array containing coordinates
        poly_coords = np.zeros((2, len(poly_r)))
        poly_coords[0, :] = poly_r
        poly_coords[1, :] = poly_z

        return poly_coords
