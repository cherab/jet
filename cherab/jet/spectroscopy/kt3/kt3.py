import numpy as np
from math import sqrt, tan, radians

from jet.data import sal

from raysect.core import Point3D, Point2D, Vector3D
from raysect.core import rotate_x, rotate_y, rotate_z
from raysect.optical.observer import FibreOptic, SpectralRadiancePipeline0D, SpectralPowerPipeline0D
from raysect.optical.loggingray import LoggingRay

from cherab.tools.observers import FibreOpticGroup
from cherab.tools.observers.spectroscopy import SpectroscopicFibreOptic


# empirically determined point limiting the inner sightlines
KT3_INNER_THRESHOLD = Point2D(3.0510967354232994, 2.0072688526617264)

def load_kt3_from_data(spectrometer, origin_rz, spots_rz, min_wavelength, max_wavelength, spectral_bins, pixel_samples=1e3,
                  toroidal_angle=303.75, parent=None):
    """
    Method returning sightlines of KT3 diagnostic as a FibreOpticGroup.

    The method uses the FibreOpticGroup to provide a set of sightlines approximating the KT3A/KT3B diagnostics. Sightlines are
    approximated with SpectroscopicFibreOptic (FibreOptic observers).
    
    :param spectrometer: Spectrometer name
    :param origin: A 1D array with [R, Z] cylindrical coordinates of the KT3 origin in the tokamak frame, which is the position
      of origin of the FibreOpticGroup.
    :param spots_rz: A 2xN array of [[R0, ...], [Z0, ...]] cylindrical coordinates in the tokaak frame of the spot centers on the tile-5 plane (divertor).
    :param min_wavelength: Minimum observed wavelength
    :param max_wavelength: Maximum observed wavelength
    :param spectral_bins: Number of spectral bins
    :param pixel_samples: Number of rays to be used in observation for every sight-line (default 1e3).
    :param toroidal_angle: The toroidal position of the diagnostic (default 303.75 degrees)
    :param parent: parent node of the returned FibreOpticGroup

    :return: FibreOpticGroup instance with sight-lines approximating KT3 diagnostic
    """

    # The spots are supposed to be "touching" the neighbout spots
    spot_radius = _calculate_spot_radii(spots_rz)
    acceptance_angles = _calculate_acceptance_angles(origin_rz, spots_rz, spot_radius)

    # the group frame is only rotated world (tokamak frame), so the transform of sightlines in
    # the group is performed in a single poloidal plane
    group = FibreOpticGroup()
    group.name = spectrometer
    group.parent = parent
    group.transform = rotate_z(toroidal_angle)
        
    origin = []
    for acceptance_angle, spot_rz in zip(acceptance_angles, spots_rz.T):
        # direction in the RZ group poloidal plane
        direction = Vector3D(spot_rz[0] - origin_rz[0], 0, spot_rz[1] - origin_rz[1])

        # Position of the observers in the RZ group poloidal plane
        # shift origin by a mm and calculate the fibre radius from the acceptance angle
        origin = Point3D(origin_rz[0], 0, origin_rz[1]) + (1e-3 * direction.normalise())
        fibre_radius = 1e-3 * tan(radians(acceptance_angle))

        sight_line = SpectroscopicFibreOptic(origin, direction, radius=fibre_radius, acceptance_angle=acceptance_angle) 
        sight_line.min_wavelength = min_wavelength
        sight_line.max_wavelength = max_wavelength
        sight_line.spectral_bins = spectral_bins
        sight_line.pixel_samples = pixel_samples

        sight_line.connect_pipelines([(SpectralRadiancePipeline0D, "radiance r:{:4.3f}".format(spot_rz[0]), None),
                                    (SpectralPowerPipeline0D, "power r:{:4.3f}".format(spot_rz[0]), None)])
        group.add_sight_line(sight_line)

    return group

def load_kt3(spectrometer, pulse_number,min_wavelength=None, max_wavelength=None, spectral_bins=None,
                 spot_position_correction=False, pulse_time=None, time_selection="nearest",
                 pixel_samples=1000, prevent_blocking=True, inner_threshold=None, parent=None):
    """
    Returns a FibreOpticGroup of observers approximating KT3 sightlines based on ppf data obtained through SAL.

    The function obtains information about the KT3 sightlines from the ppf files through Simple Acess Layer (SAL).
    The sal path to the sightline origin, spot position on tile5 and spectral data is respectively
    "/pulse/#pulse/ppf/signal/jetppf/#spectrometer/rzor", "/pulse/#shot/ppf/signal/jetppf/#spectrometer/rzdv" and
    "/pulse/#pulse/ppf/signal/jetppf/#spectrometer/wave", where the #pulse is the JET pulse number and # is t3af for
    KT3A spectrometer and t3bf for KT3B spectrometer. The spot position can be further corrected using the data from
    "/pulse/#pulse/ppf/signal/ameigs/kt3s/shfm", which gives the radial shift of the spot due to shot interference.


    It was also discovered, that sometimes the cherab sightlines can be obscured by the JET vessem models (probably
    due to a uncertainty in the origin position) A shift to the sightline origin can be applied to remove the blocking.
    The constant KT3_INNER_THRESHOLD is numerically obtained position of the bocking edge and can be recalculated using
    the determine_inner_blockpoint function.

    :param str spectrometer: Name of the spectrometer
    :param int pulse_number: JET pulse number
    :param float min_wavelength: Minimum observed wavelength to be used instead of the value provided in ppfs.
    :param float max_wavelength: Maximum observed wavelength to be used instead of the value provided in ppfs.
    :param int spectral_bins: Number of spectral bins
    :param bool spot_position_correction: If True, the radial spot position correction will be applied. If true, the 
      pulse_time parameter has to be passed. (default False)
    :param float pulse_time: Shot time to apply the radial spot position for.
    :param str time_selection: Selects the method the correction time will be selected with. If "precise", then the
      pulse_time value is matched exactly to the time values in the kt3s/shfm signal. If "nearest", then the nearest
      value to the value passed as pulse_time is provided (default "nearest").
    :param int pixel_samples: Number of sample rays to be used for every sight-line. (default 10000)
    :param bool prevent_blocking: If true, the position of the origin is shifted to avoid blocking of the inner sight-lines (default True).
    :param Point2D inner_threshold: The point setting the lowest (min(z)) outer most (max(r)) point of the limiting structure. Sight-line origins
      will be moved otwards to avoid blocking.
    :parameter parent: The parent of the returned FibreOpticGroup, (optional)
    :return: FibreOpticGroup with kt3 sight-lines
    """

    # get KT3A/KT3B data
    if spectrometer.lower() in ("a", "kt3a"):
        leaf_origin = "/pulse/{0:d}/ppf/signal/jetppf/t3af/rzor".format(int(pulse_number))
        leaf_spot_tile5 = "/pulse/{0:d}/ppf/signal/jetppf/t3af/rzdv".format(int(pulse_number))
        leaf_wave = "/pulse/{0:d}/ppf/signal/jetppf/t3af/wave".format(int(pulse_number))
        spectrometer = "KT3A"
    elif spectrometer.lower() in ("b", "kt3b"):
        leaf_origin = "/pulse/{0:d}/ppf/signal/jetppf/t3bf/rzor".format(int(pulse_number))
        leaf_spot_tile5 = "/pulse/{0:d}/ppf/signal/jetppf/t3bf/rzdv".format(int(pulse_number))
        leaf_wave = "/pulse/{0:d}/ppf/signal/jetppf/t3bf/wave".format(int(pulse_number))
        spectrometer = "KT3B"
    else:
        raise ValueError("Unkown spectrometer name")

    #get values from sal, if missing
    if not all([min_wavelength, max_wavelength, spectral_bins]):
        wave = sal.get(leaf_wave).data

        if min_wavelength is None:
            min_wavelength = wave.min() 
        
        if max_wavelength is None:
            max_wavelength = wave.max() 

        if spectral_bins is None:
            spectral_bins = wave.data.shape[0]


    toroidal_angle = 303.75

    origin_rz = sal.get(leaf_origin).data
    spots_rz = sal.get(leaf_spot_tile5).data

    if spot_position_correction:
        if not pulse_time:
            raise ValueError("Argument pulse_time has to be set for the spot position correction.")

        leaf_shift = "/pulse/{0}/ppf/signal/ameigs/kt3s/shfm".format(int(pulse_number))
        spot_shift = sal.get(leaf_shift)

        if time_selection == "nearest":
            i = np.argmin(np.abs(spot_shift.dimensions[0].data - pulse_time))
        elif time_selection == "precise":
            i = np.where(spot_shift.dimensions[0].data == pulse_time)[0]
            if i.shape[0] == 0:
                raise ValueError("Requested time is not available, consider changing the value or using time_selection='nearest'.")
        else:
            raise ValueError("Argument time_selection has to be either 'nearest' or 'precise'.")

        shift = spot_shift.data[i]

        # spot [R, Z] given in the tile5 surface plane
        # create interpolator approximating tile5 plane Z = I(R)
        tile5_interp = np.poly1d(np.polyfit(spots_rz[0, :], spots_rz[1, :], 1))
        spots_rz[0, :] += shift
        spots_rz[1, :] = tile5_interp(spots_rz[0, :])
        
    if prevent_blocking:
        inner_threshold = inner_threshold or KT3_INNER_THRESHOLD
            
        spot_radius = spots_rz[:, 1] - spots_rz[:, 0]
        spot_radius =  0.5 * sqrt(spot_radius[0] ** 2 + spot_radius[1] ** 2)
        spot_inner = Point2D(*spots_rz[:, 0])
        spot_inner.x = spot_inner.x - spot_radius
        origin_point = prevent_inner_blocking(inner_threshold, Point2D(*origin_rz), spot_inner)

        origin_rz = [origin_point.x, origin_point.y]


    return load_kt3_from_data(spectrometer, origin_rz, spots_rz, min_wavelength, max_wavelength, spectral_bins, pixel_samples, toroidal_angle,
                         parent)

def determine_inner_blockpoint(origin_rz, spot_rz_reference, parent, precision=1e-4, inner_sightline=0,
                              outer_sightline=21, initial_step=1e-2, max_iterations=100,
                              apply_margin=True):
    """
    Determines the outer most (max(r)) and lowest (min(z)) point of the blocking structure.

    :param spectrometer: Spectrometer name
    :param origin: A 1D array with [R, Z] cylindrical coordinates of the KT3 origin in the tokamak frame, which is the position
      of origin of the FibreOpticGroup.
    :param spots_rz: A 2xN array of [[R0, ...], [Z0, ...]] cylindrical coordinates in the tokaak frame of the spot centers on the tile-5 plane (divertor).
    :param parent: KT3 parent wich is in scenegraph containing the limiting structures
    :param precision: Precision with which to find the limiting point
    :param inner_sightline: Position of the inner sigh-line in the list of sightlines of the kt3 FibreOpticGroup (default 0)
    :param outer_sightline: Position of the outer sigh-line in the list of sightlines of the kt3 FibreOpticGroup (default 21)
    :param initial_step: Initial step in m to start the relaxation method with (default 1e-2m)
    :param max_iteration: Maximum number of iterations to perform
    :return: The limiting point
    """
    
    hits_inner, hits_outer, _ = _determine_limitig_point(origin_rz, spot_rz_reference, parent, precision, inner_sightline,
                              outer_sightline, initial_step, max_iterations)
    
    if hits_inner[-1][2] < 0:
        Warning("No blocking found in {:d} iteration".format(max_iterations))
    
    if hits_outer[-1][2] > 0:
        Warning("The outer sightline is blocked")
        
    threshold_point = hits_inner[-1]
    
    if apply_margin:
        #calculate radius
        r = sqrt(threshold_point[0] ** 2 + threshold_point[1] ** 2)
        # outwards offset in R
        margin_coef = (r + precision) / r
        threshold_point[0] *= margin_coef
        threshold_point[1] *= margin_coef
        # vertical offset down
        threshold_point[2] -= precision
        
    
    return Point3D(*threshold_point)

def calculate_spot_position_sightline(fibre_optic):
    """
    Calculate a hit points of a ray launched along the
    fibre_optic z axis and edges of the field of view of the fibre.

    :param fibre_optic: The FibreOptic to calculate the hit-point for.
    :return: tupple with 3x[x, y, z] coordinates for the inner, center and outer hitpoints
    """

    if not isinstance(fibre_optic, FibreOptic):
        ValueError("fibre_optic has to be of type FibreOptic")

    transform = fibre_optic.to_root() * rotate_y(1e-2)

    origin =  Point3D(0, 0, 0).transform(transform)
    direction = Vector3D(0,0, 1).transform(transform)

    logray = LoggingRay(origin=origin, direction=direction) 
    logray.trace(fibre_optic.root)
    hit_divertor = [*logray.path_vertices[-1]]

    #inner_ray
    transform = fibre_optic.to_root() * rotate_x(-fibre_optic.acceptance_angle)

    origin =  Point3D(0, 0, 0).transform(transform)
    direction = Vector3D(0,0, 1).transform(transform)

    logray = LoggingRay(origin=origin, direction=direction)
    logray.trace(fibre_optic.root)
    hit_divertor_inner = [*logray.path_vertices[-1]]

    #outer_ray
    transform = fibre_optic.to_root() * rotate_x(fibre_optic.acceptance_angle)

    origin =  Point3D(0, 0, 0).transform(transform)
    direction = Vector3D(0,0, 1).transform(transform)

    logray = LoggingRay(origin=origin, direction=direction)
    logray.trace(fibre_optic.root)
    hit_divertor_outer = [*logray.path_vertices[-1]]
    
    return hit_divertor_inner, hit_divertor, hit_divertor_outer

def prevent_inner_blocking(threshold_rz, origin_rz, spot_rz):
    """
    Shifts the origin_rz coordinates to avoid blocking of the inner sight-lines.

    The calculation is performed in cylindrical coordinates. The origin is shifted
    outwards for the sight-line edge to pass just outwards [R>R_threshold] of the point
    specified by the threshold_rz.

    :param Point3D threshold_rz: The lowest (min(Z)) and outer most (max(R)) point of the limiting structure.
    :param Point3D origin_rz: Origin of the sight-line.
    :param Point3D spot_rz: The position of the sight-line on the divertor.
    :return: The new shifted origin for which the sight-lines are not blocked.
    """

    spot_to_threshold = spot_rz.vector_to(threshold_rz)
    spot_to_origin = spot_rz.vector_to(origin_rz)


    # shift origin if the sightline edge goes above the threshold
    if spot_to_threshold.normalise().y < spot_to_origin.normalise().y:
        origin_rz =  spot_rz + (spot_to_threshold.normalise() * spot_to_origin.length)

    return origin_rz

def _determine_limitig_point(origin_rz, spot_rz_reference, parent, precision=1e-4, inner_sightline=0,
                              outer_sightline=21, initial_step=1e-2, max_iterations=100):
    """
    Determines the limiting point of the inner sightlines

    A relaxation method is applied to determine the coordinates of the edge limiting the sightlines. 
    The scenegraph kt3 is placed in has to also include the limiting structure (probably port extension of the vacuum vessel).

    :param origin_rz: A 1D array with cylindrical coordinates of the kt3 origin.
    :param spots_rz_reference: A 2xN array of [[R0, ...], [Z0, ...]] cylindrical coordinates of the spot centers on the tile-5 plane (divertor).
    :param spectral_bins: Number of spectral bins
    :param precision: Precision with which to find the limiting point
    :param inner_sightline: Position of the inner sigh-line in the list of sightlines of the kt3 FibreOpticGroup (default 0)
    :param outer_sightline: Position of the outer sigh-line in the list of sightlines of the kt3 FibreOpticGroup (default 21)
    :param initial_step: Initial step in m to start the relaxation method with (default 1e-2m)
    :param max_iteration: Maximum number of iterations to perform
    :return: The limiting point
    """

    #create a linear approximation of the tile5 surface in RZ coordinates
    tile5_interp = np.poly1d(np.polyfit(spot_rz_reference[0, :], spot_rz_reference[1, :], 1))

    spot_shift = initial_step
    shift_step = initial_step
    hit_inner = []
    hit_outer = []
    spot_shifts = []
    state = 1

    spot_rz = spot_rz_reference.copy()
    spot_rz[0, :] += spot_shift
    spot_rz[1, :] = tile5_interp(spot_rz[0, :])
    
    # Localise limiting edge with relaxation method
    for i in range(max_iterations):
        spot_rz = spot_rz_reference.copy()
        spot_rz[0, :] += spot_shift
        spot_rz[1, :] = tile5_interp(spot_rz[0, :])

        kt3 = load_kt3_from_data(origin_rz, spot_rz, min_wavelength=390, max_wavelength=412, bins_wavelength=1000, parent=parent)
        hi, _, _ = calculate_spot_position_sightline(kt3.sight_lines[inner_sightline])
        ho, _, _ = calculate_spot_position_sightline(kt3.sight_lines[outer_sightline])
        hit_inner.append(hi)
        hit_outer.append(ho)
        spot_shifts.append(spot_shift)

        #remove kt3 from the scenegraph
        #for _, fibre in kt3.fibre_optics.items():
        #    fibre.parent = None

        if abs(shift_step) < 0.5 * precision and hi[2] > 0:
            break

        if (state < 0 and hi[2] > 0 ) or (state > 0 and hi[2] < 0):
            state *= - 1
            shift_step *= -0.5

        spot_shift += shift_step
    
    if i + 1 >= max_iterations:
        raise Warning("Maximum number of iteration in search for the limiting point reached, search stopped.")
        
    return hit_inner, hit_outer, spot_shifts

def _calculate_spot_radii(spot_rz):
    """
    Calculate kt3 spot radii

    Diagnostic spots are assumed to be touching the neigbouring spots on the tile-5 plane,
    on which the spot positions are provided.

    :param spots_rz: A 2xN array of [[R0, ...], [Z0, ...]] cylindrical coordinates of the spot centers on the tile-5 plane (divertor).
    :return: 1D array of spot radii
    """

    spot_radius = np.zeros((spot_rz.shape[1]))
    diff_r = np.diff(spot_rz[0, :])
    diff_z = np.diff(spot_rz[1, :])

    spot_separation = np.sqrt(np.square(diff_r) + np.square(diff_z))


    spot_radius[0] = 0.5 * spot_separation[0]
    spot_radius[-1] = 0.5 * spot_separation[-1]

    for i, _ in enumerate(spot_separation[0: -1]):
        spot_radius[i + 1] = 0.25 * (spot_separation[i] + spot_separation[i + 1])
        
    return spot_radius

def _calculate_acceptance_angles(origin_rz, spots_rz, spot_radii):
    """
    Calculates acceptance angles for FibreOptic observers

    FibreOptic acceptance angles alpha are calculated from the position of the fibre, spot radius and spot size:

    .. math::
         \\alpha = \\arctan{\\frac{r_{fibre}}{|\mathbf{x}_{spot} - \mathbf{x}_{fibre}|}}

    where the r_fibre is the fibre radius, x_spot is the position of the spot and x_fibre is the position of the fibre.

    :param origin_rz: Mutual origin [r, z] of the sightlines in cylindrical coordinates.
    :param spots_rz: A list of 2xN [[R0, ...], [Z0, ...]] of the spot positions in cylindrical coordinates.
    :param spot_radii: A list of N spot radii
    :return: List of acceptance angles for FibreOptic observers.
    """
    
    sightline_length = np.copy(spots_rz)
    sightline_length[0, :] -= origin_rz[0]
    sightline_length[1, :] -= origin_rz[1]
    sightline_length = np.sqrt(np.sum(np.square(sightline_length), axis=0))

    return list(np.rad2deg(np.arctan(spot_radii / sightline_length)))