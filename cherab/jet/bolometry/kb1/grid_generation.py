import json
import numpy as np
from raysect.core import Point2D

from cherab.jet.machine import get_jet_wall_mask

wall_mask = get_jet_wall_mask()

xrange = (1.7, 4.0)
yrange = (-2.0, 2.0)

resolution = 0.025

nx = int(((xrange[1] - xrange[0]) / resolution))
ny = int(((yrange[1] - yrange[0]) / resolution))

num_voxels = nx * ny

xpoints = np.linspace(xrange[0], xrange[1], num=nx)
ypoints = np.linspace(yrange[0], yrange[1], num=ny)


grid_voxels = []
for ix in range(nx-1):
    for jy in range(ny-1):

        p1 = Point2D(xpoints[ix], ypoints[jy])
        p2 = Point2D(xpoints[ix], ypoints[jy+1])
        p3 = Point2D(xpoints[ix+1], ypoints[jy+1])
        p4 = Point2D(xpoints[ix+1], ypoints[jy])

        if wall_mask(*p1) or wall_mask(*p2) or wall_mask(*p3) or wall_mask(*p4):
            grid_voxels.append((p1, p2, p3, p4))

# N.B. Pickling and unpickling a ToroidalVoxelGrid is extremely inefficient:
# as well as creating a huge (~3GB) pickle file for a ~9000 voxel grid, the
# memory footprint of the ToroidalVoxelGrid trebles from 6GB to 18GB when it
# is unpickled. Possibly due to duplicating referenced objects?
#
# This means the most efficient way to store and reload the grid is to
# save just the list of list of vertices for the voxels, and then
# instantiate a ToroidalVoxelGrid with the loaded-from-json voxel data
# manually in the code which is reloading the grid.
voxel_list = [[list(p) for p in voxel] for voxel in grid_voxels]
with open('kb1_voxel_grid.json', 'w') as f:
    json.dump(voxel_list, f)
