
import os
from raysect.core import Point3D, Vector3D

from cherab.tools.observers import LineOfSightGroup, SpectroscopicSightLine


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


def load_ks5_sightlines(pulse, spectrometer, parent=None):

    print("running")

    if not pulse >= 76666:
        raise ValueError("Only shots >= 76666 are supported at this time.")

    if spectrometer not in ["ks5c", "ks5d"]:
        raise ValueError("Only spectrometers ['ks5c', 'ks5d'] are supported at this time.")

    import idlbridge as idl
    idl.execute('searchpath = !PATH')

    print('loading idl')
    global _idl_was_setup
    if not _idl_was_setup:
        print('seting up idl')
        _setup_idl()
        _idl_was_setup = True
        print('idl setup')

    print('executing idl')
    idl.execute("ret = get_ks5_alignment(pulse={}, spec='{}')".format(pulse, spectrometer))
    print('finished idl')

    # Pull out data
    cg_align = idl.get("ret")

    # Process fibres in the order that CXSfit uses.
    cxsfit_order = [i[0] for i in sorted(enumerate(cg_align['cxsfit_track']), key=lambda x:x[1], reverse=True)]

    sightline_group = LineOfSightGroup(parent=parent, name=spectrometer)

    for icg in cxsfit_order:

        fibre_name = str(cg_align['fibre_name'][icg])

        # Some fibre names are blank, meaning ignore them.
        if not fibre_name.strip():
            continue

        # Extract the fibres origin and direction
        xi = cg_align['origin_cart']['x'][icg]/1000
        yi = cg_align['origin_cart']['y'][icg]/1000
        zi = cg_align['origin_cart']['z'][icg]/1000

        pini6 = 5
        xj = cg_align['pos_activevol_cart']['x'][pini6][icg]/1000
        yj = cg_align['pos_activevol_cart']['y'][pini6][icg]/1000
        zj = cg_align['pos_activevol_cart']['z'][pini6][icg]/1000

        los_origin = Point3D(xi, yi, zi)
        los_vec = Vector3D(xj-xi, yj-yi, zj-zi).normalise()

        sight_line = SpectroscopicSightLine(los_origin, los_vec, name=fibre_name, parent=sightline_group)
        sight_line.min_wavelength = 526
        sight_line.max_wavelength = 532
        sight_line.spectral_bins = 500

        sightline_group.add_sight_line(sight_line)

    return sightline_group


if __name__ == '__main__':

    load_ks5_sightlines(87123, 'ks5c')
