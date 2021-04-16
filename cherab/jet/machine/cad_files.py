
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
from raysect.optical.library.metal import RoughTungsten, RoughBeryllium, RoughIron


try:
    CADMESH_PATH = os.environ['CHERAB_CADMESH']
except KeyError:
    if os.path.isdir('/projects/cadmesh/'):
        CADMESH_PATH = '/projects/cadmesh/'
    else:
        raise ValueError("CHERAB's CAD file path environment variable 'CHERAB_CADMESH' is"
                         "not set.")


tungsten_roughness = 0.29
beryllium_roughness = 0.26
lambertian_roughness = 0.1


# Divertor Tiles

DIV_TILE0 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile0.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE1 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile1.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE3 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile3.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE4 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile4.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5_GAP = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_gaptiles.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5_STACKA = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_StackA.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5_STACKB = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_StackB.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5_STACKC = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_StackC.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5_STACKD = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_StackD.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE5 = DIV_TILE5_GAP + DIV_TILE5_STACKA + DIV_TILE5_STACKB + DIV_TILE5_STACKC + DIV_TILE5_STACKD
DIV_TILE6 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile6.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE7 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile7.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE8 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile8.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE9 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile9.rsm'), RoughTungsten(tungsten_roughness))]
DIV_TILE10 = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile10.rsm'), RoughTungsten(tungsten_roughness))]

DIVERTOR_TILES = DIV_TILE0 + DIV_TILE1 + DIV_TILE3 + DIV_TILE4 + DIV_TILE5 + DIV_TILE6 + \
                 DIV_TILE7 + DIV_TILE8 + DIV_TILE9 + DIV_TILE10


DIV_CARRIERS = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Carriers.rsm'), Lambert(ConstantSF(0.05)))]
DIV_TILE0_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile0_structure.rsm'), Lambert(ConstantSF(0.05)))]
DIV_TILE5_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/T5_structure.rsm'), Lambert(ConstantSF(0.05)))]
DIV_TILE9_10_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/divertor/Tile9_10_structure.rsm'), Lambert(ConstantSF(0.05)))]

DIVERTOR_STRUCTURE = DIV_CARRIERS + DIV_TILE0_STRUCTURE + DIV_TILE5_STRUCTURE + DIV_TILE9_10_STRUCTURE


A2_ANTENNAS = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_Antennas.rsm'), RoughBeryllium(beryllium_roughness))]

A2_ANTENNA_TILES = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_01.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_02.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_03.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_04.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_05.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_06.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_07.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_08.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_09.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/A2_septiles_10.rsm'), RoughBeryllium(beryllium_roughness)),
]

A2 = A2_ANTENNAS + A2_ANTENNA_TILES


ILA_ANTENNA = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA.rsm'), RoughBeryllium(beryllium_roughness))]

ILA_ANTENNA_TILES = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_01L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_01M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_01R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_11M.rsm'), RoughBeryllium(beryllium_roughness)),
]

ILA_LIMMITER = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_limiter_structure.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/antennas/ILA_Limiter_Tiles.rsm'), RoughBeryllium(beryllium_roughness)),
]

ILA = ILA_ANTENNA + ILA_ANTENNA_TILES + ILA_LIMMITER


LOWER_HYBRID_ANTENNA = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/LH_Antenna.rsm'), RoughBeryllium(beryllium_roughness))]

TAE_ANTENNAS = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/TAE_Antennas.rsm'), RoughBeryllium(beryllium_roughness))]

ANTENNAS = A2 + ILA + LOWER_HYBRID_ANTENNA + TAE_ANTENNAS


INNER_WALL_BERYLLIUM_GUARD_LIMITERS = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/01L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/01ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/01M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/01MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/01R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/02ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/02MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/03ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/03MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/04ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/04MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/05ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/05MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/06ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/06MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/07ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/07MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/08L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/08ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/08MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/08R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/09L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/09ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/09MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/09R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/10L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/10ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/10MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/10R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/11L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/11ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/11M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/11MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/11R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/12L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/12ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/12M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/12MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/12R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/13L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/13ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/13M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/13MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/13R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/14L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/14ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/14M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/14MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/14R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/15L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/15ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/15M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/15MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/15R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/16L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/16ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/16M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/16MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/16R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/17L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/17ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/17M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/17MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/17R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/18L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/18ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/18M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/18MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/18R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/19L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/19ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/19M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/19MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Be/19R.rsm'), RoughBeryllium(beryllium_roughness)),
]

INNER_WALL_TUNGSTEN_GUARD_LIMITERS = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/01L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/01R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/02L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/02L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/02R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/02R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/03L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/03L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/03R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/03R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/04L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/04L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/04R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/04R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/05L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/05L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/05R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/05R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/06L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/06L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/06R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/06R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/07L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/07L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/07R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/07R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/08L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/08L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/08R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/08R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/09L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/09L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/09R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/09R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/10L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/10L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/10R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/10R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/11L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/11L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/11R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/11R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/12L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/12L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/12R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/12R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/13L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/13L_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/13R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/13R_inset.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/14B_L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/14B_R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/14L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/14R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/15B_L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/15B_R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/15L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/15R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/Bottom_L.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/Bottom_R.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_01.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_02.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_03.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_04.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_05.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_06.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_07.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_08.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_09.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_10.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_11.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_12.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_13.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_14.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_15.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/RW_16.rsm'), RoughTungsten(tungsten_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Tiles_Wc/Top.rsm'), RoughTungsten(tungsten_roughness)),
]

IWGL_CARRIERS = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_carriers.rsm'), Lambert(ConstantSF(0.05)))]

IWGL_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IWGL_Structure.rsm'), Lambert(ConstantSF(0.05)))]

INNER_WALL_GUARD_LIMITERS = INNER_WALL_BERYLLIUM_GUARD_LIMITERS + INNER_WALL_TUNGSTEN_GUARD_LIMITERS + IWGL_CARRIERS + IWGL_STRUCTURE

INNER_WALL_CLADDING_TILES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IW_Cladding_Tiles.rsm'), Lambert(ConstantSF(lambertian_roughness)))]
# INNER_WALL_CLADDING_TILES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IW_Cladding_Tiles.rsm'), RoughBeryllium(beryllium_roughness))]


OPL_TILES = [
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_01L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_01M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_01R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_08L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_08R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_09L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_09R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_10L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_10R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_11L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_11M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_11R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_12L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_12M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_12R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_13L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_13M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_13R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_14L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_14M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_14R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_15L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_15M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_15R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_16L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_16M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2B_16R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_01L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_01M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_01R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_08L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_08R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_09L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_09R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_10L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_10R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_11L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_11M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_11R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_12L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_12M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_12R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_13L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_13M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_13R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_14L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_14M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_14R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_15L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_15M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_15R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_16L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_16M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/2D_16R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_01.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_08L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_08R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_09L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_09R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_10L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_10R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_11L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_11M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_11R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_12L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_12M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_12R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_13L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_13M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_13R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_14L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_14M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_14R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_15L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_15M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_15R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_16L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_16M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_16R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_17L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_17M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_17R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_18L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_18M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_18R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_19L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_19M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_19R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_20L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_20M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_20R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_21L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_21M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_21R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_22L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_22M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_22R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/3B_23.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w01.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w02RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w03RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w04RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w05RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w06RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w07RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w08RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w09RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w10RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w11RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w12RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w13RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w14RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w15RWobj.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w16RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w17RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w18RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w19RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w20RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w21RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22L.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22LW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22M.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22ML.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22MR.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22R.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w22RW.rsm'), RoughBeryllium(beryllium_roughness)),
    (os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Tiles_Be/w23.rsm'), RoughBeryllium(beryllium_roughness)),
]

OPL_TILE_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OPL_Structure.rsm'), Lambert(ConstantSF(lambertian_roughness)))]

UDP_TILES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/UDP_Tiles.rsm'), RoughBeryllium(beryllium_roughness))]

UO_SC = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/UO_SC.rsm'), RoughIron(0.05))]

OL_SC = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/OL_SC.rsm'), RoughIron(0.05))]

MUSHROOM_TILES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/Mushrooms.rsm'), RoughBeryllium(beryllium_roughness))]

SAUSAGES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/Sausages.rsm'), RoughBeryllium(beryllium_roughness))]

IL_SAUSAGES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IL_Sausages.rsm'), RoughBeryllium(beryllium_roughness))]

SC_XOVER = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/SC_Xover.rsm'), RoughIron(0.05))]

REION_PLATES = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/REION_plates.rsm'), RoughTungsten(tungsten_roughness))]


VACUUM_VESSEL = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/Vacuum_vessel.rsm'), Lambert(ConstantSF(lambertian_roughness)))]

DIAGNOSTICS = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/Diagnostics.rsm'), Lambert(ConstantSF(lambertian_roughness)))]

COOLING_MANIFOLD = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/Cooling_Manifold.rsm'), Lambert(ConstantSF(lambertian_roughness)))]

IL_SC = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IL_SC.rsm'), RoughIron(0.05))]

IL_SC_STRUCTURE = [(os.path.join(CADMESH_PATH, 'jet/v1.1/rsm/IL_SC_Structure.rsm'), Lambert(ConstantSF(lambertian_roughness)))]


# Complete JET mesh for first wall reflection calculations
JET_MESH = ANTENNAS + INNER_WALL_GUARD_LIMITERS + INNER_WALL_CLADDING_TILES + OPL_TILES + OPL_TILE_STRUCTURE + \
           UDP_TILES + UO_SC + OL_SC + MUSHROOM_TILES + SAUSAGES + IL_SAUSAGES + SC_XOVER + REION_PLATES + \
           VACUUM_VESSEL + DIAGNOSTICS + IL_SC + IL_SC_STRUCTURE + DIVERTOR_TILES + DIVERTOR_STRUCTURE


def import_jet_mesh(world, override_material=None, tungsten_material=None, beryllium_material=None,
                    lambert_material=None, verbose=True, mesh_description=JET_MESH):
    """ Imports JET machine meshes.

    Args:
        :param world: The parent node.
        :param override_material: Optional, overrides materials specified in the mesh_description.
        :param tungsten_material: Optional, overrides tungsten materials specified in mesh_description.
        :param beryllium_material: Optional, overrides beryllium materials specified in mesh_description.
        :param lambert_material: Optional, overrides Lambertian materials specified in mesh_description.
        :param verbose: Sets the verbosity, defaults True.
        :param mesh_description: Optional, list of tupples of the shape (mesh file path, material). On default equals to the
                                 JET_MESH list.
    """
    
    for mesh_item in mesh_description:

        mesh_path, default_material = mesh_item

        if override_material:
            material = override_material
        elif tungsten_material and isinstance(default_material, RoughTungsten):
            material = tungsten_material
        elif beryllium_material and isinstance(default_material, RoughBeryllium):
            material = beryllium_material
        elif lambert_material and isinstance(default_material, Lambert):
            material = lambert_material
        else:
            material = default_material

        if verbose:
            print("importing {}  ...".format(os.path.split(mesh_path)[1]))
        directory, filename = os.path.split(mesh_path)
        mesh_name, ext = filename.split('.')
        Mesh.from_file(mesh_path, parent=world, material=material, name=mesh_name)


###########################
# DIAGNOSTICS

KB5V = [(os.path.join(CADMESH_PATH, 'jet/rsm/diagnostics/KB5/KB5V/kb5v.obj'), RoughTungsten(tungsten_roughness))]
KB5H = [(os.path.join(CADMESH_PATH, 'jet/rsm/diagnostics/KB5/KB5H/kb5h.obj'), RoughTungsten(tungsten_roughness))]
