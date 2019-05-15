
import pickle
import os
import numpy as np
from raysect.core import Point2D

from cherab.jet.machine import get_jet_wall_mask
from cherab.jet.bolometry.kb1 import load_kb1


wall_mask = get_jet_wall_mask()

xrange = (1.7, 4.0)
yrange = (-2.0, 2.0)

resolution = 0.025

nx = round(((xrange[1] - xrange[0]) / resolution))
ny = round(((yrange[1] - yrange[0]) / resolution))

num_voxels = nx * ny

# Coordinate of vertices
xpoints = np.linspace(xrange[0], xrange[1], num=nx + 1)
ypoints = np.linspace(yrange[0], yrange[1], num=ny + 1)

grid_index_2D_to_1D_map = {}
grid_index_1D_to_2D_map = {}

grid_cells = []
unwrapped_cell_index = 0
for ix in range(nx-1):
    for jy in range(ny-1):

        p1 = Point2D(xpoints[ix], ypoints[jy])
        p2 = Point2D(xpoints[ix], ypoints[jy+1])
        p3 = Point2D(xpoints[ix+1], ypoints[jy+1])
        p4 = Point2D(xpoints[ix+1], ypoints[jy])

        if wall_mask(*p1) or wall_mask(*p2) or wall_mask(*p3) or wall_mask(*p4):
            grid_cells.append((p1, p2, p3, p4))
            grid_index_2D_to_1D_map[(ix, jy)] = unwrapped_cell_index
            grid_index_1D_to_2D_map[unwrapped_cell_index] = (ix, jy)
            unwrapped_cell_index += 1


num_cells = len(grid_cells)
cell_data = np.zeros((num_cells, 4, 2))
for i in range(num_cells):
    p1, p2, p3, p4 = grid_cells[i]
    cell_data[i, 0, :] = p1.x, p1.y
    cell_data[i, 1, :] = p2.x, p2.y
    cell_data[i, 2, :] = p3.x, p3.y
    cell_data[i, 3, :] = p4.x, p4.y


kb1_grid = {
    'voxels': grid_cells,
    'index_2D_to_1D_map': grid_index_2D_to_1D_map,
    'index_1D_to_2D_map': grid_index_1D_to_2D_map,
}

# Save the files in the same directory as the loader module
directory = os.path.split(load_kb1.__file__)[0]
file_name = "kb1_voxel_grid.pickle"
file_path = os.path.join(directory, file_name)
with open(file_path, "wb") as f:
    pickle.dump(kb1_grid, f)
