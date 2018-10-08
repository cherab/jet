
import numpy as np
from raysect.core import Point2D

from cherab.tools.observers.inversion_grid import RectangularGrid
from cherab.jet.machine import get_jet_wall_mask, plot_jet_wall_outline


wall_mask = get_jet_wall_mask()

xrange = (1.7, 4.0)
yrange = (-2.0, 2.0)

resolution = 0.025

nx = int(((xrange[1] - xrange[0]) / resolution))
ny = int(((yrange[1] - yrange[0]) / resolution))

num_voxels = nx * ny

xpoints = np.linspace(xrange[0], xrange[1], num=nx)
ypoints = np.linspace(yrange[0], yrange[1], num=ny)


grid_cells = []
for ix in range(nx-1):
    for jy in range(ny-1):

        p1 = Point2D(xpoints[ix], ypoints[jy])
        p2 = Point2D(xpoints[ix], ypoints[jy+1])
        p3 = Point2D(xpoints[ix+1], ypoints[jy+1])
        p4 = Point2D(xpoints[ix+1], ypoints[jy])

        if wall_mask(*p1) or wall_mask(*p2) or wall_mask(*p3) or wall_mask(*p4):
            grid_cells.append((p1, p2, p3, p4))


num_cells = len(grid_cells)
cell_data = np.zeros((num_cells, 4, 2))
for i in range(num_cells):
    p1, p2, p3, p4 = grid_cells[i]
    cell_data[i, 0, :] = p1.x, p1.y
    cell_data[i, 1, :] = p2.x, p2.y
    cell_data[i, 2, :] = p3.x, p3.y
    cell_data[i, 3, :] = p4.x, p4.y

kb5_grid = RectangularGrid('JET KB5 inversion grid', cell_data)
kb5_grid.save('kb5_inversion_grid.json')


# import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection
# patches = []
# for i in range(num_cells):
#     polygon = Polygon(kb5_grid.cell_data[i], True)
#     patches.append(polygon)
# p = PatchCollection(patches)
#
# fig, ax = plt.subplots()
# ax.add_collection(p)
# plot_jet_wall_outline()
# plt.xlim(*xrange)
# plt.ylim(*yrange)
# plt.show()
