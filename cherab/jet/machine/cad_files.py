
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

from raysect.primitive import Mesh
from raysect.optical.spectralfunction import ConstantSF
from raysect.optical.material import AbsorbingSurface, Lambert
from raysect.optical.library.metal import RoughTungsten


try:
    CADMESH_PATH = os.environ['CHERAB_CADMESH']
except KeyError:
    raise ValueError("CHERAB's CAD file path environment variable 'CHERAB_CADMESH' is"
                     "not set.")


METAL_PARTS = [
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/A2_Antennas.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/B_C_tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/DP_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/GB_Carrier_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/High Field Gap_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/ICRD.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/ICRH_PL_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/IL_SC.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/IWGL_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/IWP_tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/LBSRP_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/LHCD.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/LO_SC.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/Lost_Apha.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/Mushroom_Tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/PL_tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/TAE.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/UIWP_tiles.rsm'), RoughTungsten(0.2)),
    (os.path.join(CADMESH_PATH, 'jet/rsm/metal/UO_SC.rsm'), RoughTungsten(0.2)),
]

DARK_PARTS = [
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/B_C_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Coil_Conduit.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Cooling_Manifold.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Diagnostics.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/DP_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/DS.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/ICRH_PL_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/IWGL_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/IWP_structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/KE14.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/LHCD_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Mushroom_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Oct4_Glow_Discharge.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/PL_Structure.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/SC_Feeds.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/SC_Xover.rsm'), Lambert(ConstantSF(0.25))),
    (os.path.join(CADMESH_PATH, 'jet/rsm/dark/Vessel Wall.rsm'), Lambert(ConstantSF(0.25))),
]


JET_MESH = METAL_PARTS + DARK_PARTS


def import_jet_mesh(world, material=None):

    for mesh_item in JET_MESH:

        mesh_path, default_material = mesh_item

        if not material:
            material = default_material

        print("importing {}  ...".format(os.path.split(mesh_path)[1]))
        directory, filename = os.path.split(mesh_path)
        mesh_name, ext = filename.split('.')
        Mesh.from_file(mesh_path, parent=world, material=material, name=mesh_name)


