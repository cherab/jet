
# External imports
from math import factorial
import collections

import ppf
import numpy as np

# Internal imports
from cherab.core.math.interpolators import Interpolate1DCubic


# TODO - Make a set of base classes for types of measured/profile data
class MeasuredProfile:
    pass


# TODO - This class is really terrible and hacky. Was trying to get something done quickly. Will need to come back to
# this and fix all the problems.
class JETMeasuredProfile:

    def __init__(self, name, shot, diag_code, var_code, equilibrium, errvar_code=None, radius_code=None,
                 filtered_profile=False, start_time=None, ppfuid='JETPPF', seq=0, z_code=None, border=None):
        """

        :param name: A name for this set of reference data.
        :param shot: A machine reference number, i.e. shot/pulse number.
        :param diag_code: A diagnostic reference code, i.e. 'HRTS'
        :param var_code: A specific physics variable code, i.e.
        :param equilibrium: JET equilibrium object.
        :param errvar_code: An optional variable code for accessing error data.
        :param str ppfuid: User ID for this PPF.
        :param int seq: Sequence number for this ppf.
        :param str z_code: (optional) code (dtype) to read z position.
        :param dict border: (optional) If is not set, its value is
            {'type': 'fixed', 'value': 0.0}). border should have a key 'type'
            which can be: 'fixed', 'free', 'factor':
            'fixed', for psi=1, border['value'];
            'free', there is no given value for psi=1;
            'factor', for psi=1, is value is last_value * border['value']
        """

        self.name = name
        ppf.ppfuid(ppfuid, rw='R')
        ppf.ppfgo(pulse=shot, seq=seq)
        _, _, data, x, t, _ = ppf.ppfget(shot, diag_code, var_code)
        if len(t) < 1:
            raise RuntimeError("No ppf data available for pulse {}, diagnostic {}, variable {}."
                               "".format(shot, diag_code, var_code))
        if z_code:
            _, _, z, _, _, ierr = ppf.ppfget(shot, diag_code, z_code)
            if ierr != 0:
                raise RuntimeError("No ppf z available for pulse {}, diagnostic {}, variable {}."
                                   "".format(shot, diag_code, z_code))
            if z.size > len(x):
                z = z.reshape(len(t), len(x))
        else:
            z = x.copy()
            z[:] = 0
        self._data = data.reshape(len(t), len(x))

        if radius_code:
            _, _, rdata, _, _, _ = ppf.ppfget(shot, diag_code, radius_code)
            self._rdata = rdata.reshape(len(t), len(x))
        else:
            self._rdata = x

        self.time = t
        self._z = z
        self._equilibrium = equilibrium
        self.filtered_profile = filtered_profile

        if errvar_code and isinstance(errvar_code, tuple):
            err_low_code, err_high_code = errvar_code
            _, _, edata_low, x, t, _ = ppf.ppfget(shot, diag_code, err_low_code)
            self._edata_low = edata_low.reshape(len(t), len(x))
            _, _, edata_high, x, t, _ = ppf.ppfget(shot, diag_code, err_high_code)
            self._edata_high = edata_high.reshape(len(t), len(x))
            self._edata = (self._edata_high - self._edata_low)/2

        elif errvar_code:
            _, _, edata, x, t, _ = ppf.ppfget(shot, diag_code, errvar_code)
            self._edata = edata.reshape(len(t), len(x))
        else:
            self._edata = None

        self._border = border if border else {'type': 'fixed', 'value': 0.0}

        if start_time:
            self.move_time_curser_to(start_time)
        else:
            self.move_time_curser_to(t[0])

    def __call__(self, psi):

        if isinstance(psi, (collections.Sequence, np.ndarray)):
            result = []
            for psi_i in psi:
                if 0 <= psi_i <= 1:
                    result.append(self._profile(psi_i))
                else:
                    raise ValueError("Psi must be between 0 <= psi <= 1.")
            return result
        else:
            return self._profile(psi)

    @property
    def data(self):
        return self._data[self.time_cursor[0]]

    @property
    def edata(self):
        return self._edata[self.time_cursor[0]]

    @property
    def edata_low(self):
        try:
            return self._edata_low[self.time_cursor[0]]
        except AttributeError:
            raise RuntimeError("No lower bound error data available.")

    @property
    def edata_high(self):
        try:
            return self._edata_high[self.time_cursor[0]]
        except AttributeError:
            raise RuntimeError("No upper bound error data available.")

    @property
    def radii(self):
        if self._rdata.ndim == 2:
            return self._rdata[self.time_cursor[0]]
        else:
            return self._rdata

    @property
    def z(self):
        if self._z.ndim == 2:
            z = self._z[self.time_cursor[0]]
        else:
            z = self._z
        return z

    # TODO - this is messy and should be cleaned up
    def move_time_curser_to(self, time):
        if not self.time[0] <= time <= self.time[-1]:
            raise ValueError("Time {} is outside of the time axis range.".format(time))

        index = self._get_index_closest_to_time(time)
        time = self.time[index]
        self.time_cursor = (index, time)

        if self.filtered_profile:
            y = savitzky_golay(self._data[index, :], 5, 3)
        else:
            y = self._data[index]

        psi = []
        yy = []

        # Magnetic coordinates best at measurement time
        psin = self._equilibrium.time(time).psi_normalised
        for i, (r, z) in enumerate(zip(self.radii, self.z)):
            # TODO - this was introduced to fix a bug due to duplicate psi values, which shouldn't be possible!
            # Need to chase this up.
            p = psin(r, z)
            if p in psi or p >= 0.99:
                continue
            psi.append(p)
            if y[i] < 0:
                yy.append(0.0)
            else:
                yy.append(y[i])

        self.psi_current = np.array(psi)
        self.y_current = np.array(yy)

        border = self._border
        if border['type'] != 'free':
            # Set last value
            psi.append(1.0)
            if border['type'] == 'fixed':
                yy.append(border['value'])
            elif border['type'] == 'factor':
                yy.append(yy[-1] * border['value'])
            else:
                raise ValueError('Wrong border type: {}'.format(border['type']))

        self._profile = Interpolate1DCubic(psi, yy, extrapolate=True)

    def _get_index_closest_to_time(self, time):
        return np.abs(self.time - time).argmin()


# Developed from scipy public cookbook
# Source: http://wiki.scipy.org/Cookbook/SavitzkyGolay
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    """
    Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.

    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)

    Returns
    -------
    ys : ndarray, shape (N)
         the smoothed signal (or it's n-th derivative).

    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.

    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
    Data by Simplified Least Squares Procedures. Analytical
    Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
    W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
    Cambridge University Press ISBN-13: 9780521880688
    """

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")

    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")

    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")

    order_range = range(order+1)
    half_window = (window_size -1) // 2

    # pre-compute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)

    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))

    return np.convolve(m[::-1], y, mode='valid')
