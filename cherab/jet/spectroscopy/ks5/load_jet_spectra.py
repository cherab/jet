
# TODO - This file is a horrible mess, but not my fault...
# Needs a major re-write

# External imports
import os
import numpy as np
from raysect.core.math import Point3D, Vector3D, Point2D

# Internal imports
from cherab.core.math.interpolators import Interpolate1DCubic
from cherab.fitting.fit_strategy import fit_instrument_width
from cherab.fitting.spectra import TimeSeriesSpectra
from cherab.fitting.lines_of_sight import LOSGroup, LineOfSight


_idl_was_setup = False


def _setup_idl():

    import idlbridge as idl

    module_path = os.path.abspath(os.path.dirname(__file__))

    idl.execute('searchpath = !PATH')
    searchpath = idl.get('searchpath')

    if searchpath.find(module_path) == -1:
        idl.execute("!PATH=!PATH + ':' + '{}'".format(module_path))

    if searchpath.find('cxs/ks6read') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/ks6read/' )")

    if searchpath.find('cxs/ktread') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/ktread/' )")

    if searchpath.find('cxs/kx1read') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/kx1read/' )")

    if searchpath.find('cxs/idl_spectro/kt3d') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/idl_spectro/kt3d' )")

    if searchpath.find('cxs/utc') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/utc' )")

    if searchpath.find('cxs/instrument_data') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/instrument_data' )")

    if searchpath.find('cxs/calibration') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/calibration' )")

    if searchpath.find('cxs/utilities') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/utilities' )")

    if searchpath.find('cxs/idl/ks457_0/programs') == -1:
        idl.execute("!PATH=!PATH + ':' + expand_path( '+~cxs/idl/ks457_0/programs/')")


def load_jet_spectra(pulse, spec, los_list=None, psi_fn=False, check_errors=False, background_range=None,
                     print_fit=False, plot=False, frames_to_average=None, desmearing=False):

    if pulse < 76666:
        raise ValueError("Shot {} is incompatible at this time.".format(pulse))

    if spec not in ["ks5c", "ks5d"]:
        raise ValueError("Spec {} is incompatible at this time.".format(spec))

    global _idl_was_setup
    if not _idl_was_setup:
        _setup_idl()
        _idl_was_setup = True
    samples, errors, wvlths, times, amdatatrack, cg_align, inst_data, inst_wave = from_idl(pulse, spec)

    print('sample size -> {}'.format(samples.shape))
    if desmearing:
        raw_samples = samples.copy()
        num_tracks = samples.shape[1]
        smearing_fraction = 0.5 / 10 / num_tracks

        for i in range(len(times)):
            # Sum up the light from all tracks at this time slice, divide by smearing time fraction
            frame_smear = np.sum(raw_samples[i, :, :], axis=0) * smearing_fraction
            for j in range(num_tracks):
                samples[i, j, :] = raw_samples[i, j, :] - frame_smear

    los_group = LOSGroup(spec)

    # Creat mapping functions for mapping los radii to midplane
    xc = 3.017  # approximate radius of equilibrium centre point.
    hc = 0.327  # approximate height of equilibrium centre point.
    xedge = 0.0  # approximate edge radius of plasma
    r = xc
    psi_values = []
    r_values = []

    while psi_fn(r, 0, hc) <= 1.0 and r < 4.0:
        psi_values.append(psi_fn(r, 0, hc))
        r_values.append(r)
        r += 0.02
        if psi_fn(r, 0, hc) >= 1.0:
            xedge = r

    psi_to_major_r = Interpolate1DCubic(psi_values, r_values, extrapolate=True)

    # Process fibres in the order that CXSfit uses.
    cxsfit_order = [i[0] for i in sorted(enumerate(cg_align['cxsfit_track']), key=lambda x:x[1], reverse=True)]

    for icg in cxsfit_order:

        fibre_name = str(cg_align['fibre_name'][icg])

        # TODO - ugly code to get the correct data track, this really needs to be cleaned up.
        cgtrack = cg_align['track'][icg]
        index = np.where(amdatatrack == cgtrack)[0][0]

        # Some fibre names are blank, meaning ignore them.
        if not fibre_name.strip():
            continue

        # Only process fibres that we want to use:
        if los_list:
            if fibre_name not in los_list:
                continue

        # Load and process instrument function data for this channel
        inst_width = fit_instrument_width(inst_wave[index, :], inst_data[index, :], print_fit=print_fit, plot_fit=plot)

        # Create a time series of spectra for this fibre.
        if not frames_to_average:
            spectra = TimeSeriesSpectra(wvlths[index, :], samples[:, index, :], errors[:, index, :], times,
                                        inst_sigma=inst_width, name=fibre_name, background_range=background_range)
        else:
            frames_to_average = int(frames_to_average)
            n_times, n_indices, n_samples = samples.shape
            n_avg_times = int(np.floor(n_times/frames_to_average))

            r_samples = np.reshape(samples[:, index, :], (-1, frames_to_average, n_samples))
            r_errors = np.reshape(errors[:, index, :], (-1, frames_to_average, n_samples))
            r_times = np.reshape(times, (-1, frames_to_average))

            avg_samples = np.mean(r_samples, axis=1)
            avg_errors = np.mean(r_errors, axis=1)
            avg_times = np.mean(r_times, axis=1)

            spectra = TimeSeriesSpectra(wvlths[index, :], avg_samples, avg_errors, avg_times,
                                        inst_sigma=inst_width, name=fibre_name, background_range=background_range)

        # Checks that the errors given are reasonable.
        if check_errors:
            spectra.check_errors()

        # Extract the fibres origin and direction
        xi = cg_align['origin_cart']['x'][icg]/1000
        yi = cg_align['origin_cart']['y'][icg]/1000
        zi = cg_align['origin_cart']['z'][icg]/1000

        pini6 = 5
        xj = cg_align['pos_activevol_cart']['x'][pini6][icg]/1000
        yj = cg_align['pos_activevol_cart']['y'][pini6][icg]/1000
        zj = cg_align['pos_activevol_cart']['z'][pini6][icg]/1000

        radius = cg_align['pos_activevol']['r'][pini6][icg]/1000

        # Find radius mapped to midplane
        psi_at_intersection = psi_fn(xj, yj, zj)
        if psi_at_intersection <= 1.0:
            radius = psi_to_major_r(psi_at_intersection)
            rho = (radius - xc) / (xedge - xc)  # find normalised major radius in range -1 < r/a < 1.
            # Try to catch case where sight line is on other side of magnetic axis.
            if r < xc:
                radius = xc - (radius - xc)
                rho = -rho

        # Extract the active volume calibration factor
        active_volume = cg_align['activevol'][pini6][icg]

        # TODO - Alex pointed out that this needs to be more flexible.
        los_origin = Point3D(xi, yi, zi)
        pini_intersection = Point3D(xj, yj, zj)
        los_vec = Vector3D(xj-xi, yj-yi, zj-zi)
        los_vec = los_vec.normalise()

        # Find local toroidal rotation vector at pini intersection point
        trot_vec = Vector3D(-pini_intersection.y, pini_intersection.x, 0.0)
        trot_vec = trot_vec.normalise()

        theta_los = np.rad2deg(np.arccos(trot_vec.dot(los_vec)))

        # Calculation of PCX LOS angle
        try:
            start = los_origin
            end = los_origin + los_vec
            dx = end.x - start.x
            dy = end.y - start.y
            dr = np.sqrt(dx*dx + dy*dy)
            det = start.x * end.y - end.x * start.y
            disc = xedge**2 * dr**2 - det**2

            if disc <= 0:
                raise RuntimeError("Imaginary solution found...")

            los_direction = Vector3D(los_vec.x, los_vec.y, 0.0).normalise()

            x = (det*dy + np.sign(dy) * dx * np.sqrt(disc)) / dr**2
            y = (-det*dx + abs(dy) * np.sqrt(disc)) / dr**2
            point_a = Point2D(x, y)
            trot_vec_a = Vector3D(-point_a.y, point_a.x, 0.0).normalise()
            pcx_theta = np.rad2deg(np.arccos(trot_vec_a.dot(los_direction)))

        except RuntimeError:
            pcx_theta = None

        los = LineOfSight(fibre_name, spectra, los_origin, los_vec, psi_fn, radius=radius, point_of_interest=pini_intersection,
                          active_volume=active_volume, theta_los=theta_los, pcx_theta=pcx_theta)
        los_group.add_los(los)

    return los_group


def from_idl(pulse, spec):
    import idlbridge as idl
    idl.execute("ret = get_ks5data(pulse={}, spec='{}')".format(pulse, spec))

    # Pull out data
    ret = idl.get("ret")
    samples = ret['data']
    errors = ret['error']
    wvlths = ret['wave_cal']  # Wavelengths
    times = ret['time']
    cg_align = ret['cg_align']
    amdatatrack = ret['datatrack']
    inst_data = ret['inst_data']
    inst_wave = ret['inst_wave']

    return samples, errors, wvlths, times, amdatatrack, cg_align, inst_data, inst_wave
