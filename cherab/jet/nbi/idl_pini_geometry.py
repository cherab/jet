
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

import os
from numpy import pi as PI
from raysect.core import Point3D, Vector3D


# NIB8 PINIs lengths (distance from the source in meters)
PINI_LENGTHS = [16.10934611, 15.48338613, 11.57900764, 11.60077588, 11.47816349, 11.44278883, 15.90863813, 16.31158651]

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

    # idl_path = "!PATH=!PATH + ':' + expand_path( '+~cxs/ks6read/' ) + ':' + expand_path( '+~cxs/ktread/' ) + ':' + " \
    #            "expand_path( '+~cxs/kx1read/' ) + ':' + expand_path( '+~cxs/idl_spectro/kt3d' ) + ':' + " \
    #            "expand_path( '+~cxs/utc' ) + ':' + expand_path( '+~cxs/instrument_data' ) + ':' + " \
    #            "expand_path( '+~cxs/calibration' ) + ':' + expand_path( '+~cxs/utilities' ) + ':' + " \
    #            "expand_path( '+~cxs/idl/ks457_0/programs/') + ':' + '{}'".format(ks5_idl_path)
    # idl.execute(idl_path)


def get_pini_alignment(pulse, oct8_pini):

    import idlbridge as idl

    global _idl_was_setup
    if not _idl_was_setup:
        _setup_idl()
        _idl_was_setup = True

    # Note: array index starts at zero, so actual pini index equals pini number - 1/.
    oct8_pini -= 1

    idl.execute("ret = get_cherab_pinialignment(pulse={})".format(pulse))
    ret = idl.get("ret")

    # Pull out the origin points from the IDL structure, convert to Point3D
    origin = Point3D(ret['origin'][oct8_pini][0]/1000, ret['origin'][oct8_pini][1]/1000, ret['origin'][oct8_pini][2]/1000)

    # Pull out the direction vector from the IDL structure, convert to Vector3D
    direction = Vector3D(ret['vector'][oct8_pini][0], ret['vector'][oct8_pini][1], ret['vector'][oct8_pini][2])

    # TODO - note divergence numbers are different between Carine and Corentin.
    div_u = ret['divu'][oct8_pini]/(2*PI)*360
    div_v = ret['divv'][oct8_pini]/(2*PI)*360
    divergence = (div_u, div_v)

    # Minimal 1/e width (at the source) of the beam (scalar in meters)
    initial_width = 0.001  # Approximate with 1mm as an effective point source.

    pini_length = PINI_LENGTHS[oct8_pini]

    pini_geometry = (origin, direction, divergence, initial_width, pini_length)

    return pini_geometry


if __name__ == '__main__':

    t = get_pini_alignment(87123, 6)
    print(t)
