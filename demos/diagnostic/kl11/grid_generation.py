
import csv
import numpy as np
import matplotlib.pyplot as plt
from raysect.core import Point2D
from scipy.sparse import csc_matrix

from cherab.tools.inversions import ToroidalVoxelGrid
from cherab.jet.machine import get_jet_wall_mask, plot_jet_wall_outline
from cherab.jet.equilibrium import JETEquilibrium


wall_mask = get_jet_wall_mask()

pulse_equilibrium = JETEquilibrium(93134)
inside_lcfs = pulse_equilibrium.time(48.0).inside_lcfs
psi_normalised = pulse_equilibrium.time(48.0).psi_normalised


xrange = (1.84, 3.88)
yrange = (-1.8, 1.80)

div_xrange = (2.3, 3.0)
div_yrange = (-1.8, -1.2)

resolution = 0.01
nx = int(((xrange[1] - xrange[0]) / resolution))
ny = int(((yrange[1] - yrange[0]) / resolution))

num_voxels = nx * ny

xpoints = np.linspace(xrange[0], xrange[1], num=nx)
ypoints = np.linspace(yrange[0], yrange[1], num=ny)
bool_mask = np.empty((nx, ny), dtype=bool)


unwrapped_cell_index = 0
grid_cells = []
grid_index_2D_to_1D_map = {}
grid_index_1D_to_2D_map = {}
for ix in range(nx-1):
    print("{:.3G} % complete".format(ix / (nx-1) * 100))
    for jy in range(ny-1):

        p1 = Point2D(xpoints[ix], ypoints[jy])
        p2 = Point2D(xpoints[ix], ypoints[jy+1])
        p3 = Point2D(xpoints[ix+1], ypoints[jy+1])
        p4 = Point2D(xpoints[ix+1], ypoints[jy])

        # Divertor criteria
        if p1.y < div_yrange[1] and div_xrange[0] <= p1.x <= div_xrange[1]:
            if wall_mask(*p1) or wall_mask(*p2) or wall_mask(*p3) or wall_mask(*p4):
                grid_cells.append((p1, p2, p3, p4))
                bool_mask[ix, jy] = True
                grid_index_2D_to_1D_map[(ix, jy)] = unwrapped_cell_index
                grid_index_1D_to_2D_map[unwrapped_cell_index] = (ix, jy)
                unwrapped_cell_index += 1
            else:
                bool_mask[ix, jy] = False

        # core criteria
        else:
            num_points_inside = 0
            for p in [p1, p2, p3, p4]:
                if 0.99 <= psi_normalised(p.x, p.y) <= 1.05:
                    num_points_inside += 1
            if num_points_inside >= 1 and wall_mask(*p1):
                grid_cells.append((p1, p2, p3, p4))
                bool_mask[ix, jy] = True
                grid_index_2D_to_1D_map[(ix, jy)] = unwrapped_cell_index
                grid_index_1D_to_2D_map[unwrapped_cell_index] = (ix, jy)
                unwrapped_cell_index += 1
            else:
                bool_mask[ix, jy] = False


plt.ion()
kl11_grid = ToroidalVoxelGrid(grid_cells, 'JET KL11 grid')
kl11_grid.plot()
plot_jet_wall_outline()


grid_laplacian = np.zeros((kl11_grid.count, kl11_grid.count))
for ith_cell in range(kl11_grid.count):

    # get the 2D mesh coordinates of this cell
    ix, iy = grid_index_1D_to_2D_map[ith_cell]

    neighbours = 0

    try:
        n1 = grid_index_2D_to_1D_map[ix-1, iy]  # neighbour 1
        grid_laplacian[ith_cell, n1] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n2 = grid_index_2D_to_1D_map[ix-1, iy+1]  # neighbour 2
        grid_laplacian[ith_cell, n2] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n3 = grid_index_2D_to_1D_map[ix, iy+1]  # neighbour 3
        grid_laplacian[ith_cell, n3] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n4 = grid_index_2D_to_1D_map[ix+1, iy+1]  # neighbour 4
        grid_laplacian[ith_cell, n4] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n5 = grid_index_2D_to_1D_map[ix+1, iy]  # neighbour 5
        grid_laplacian[ith_cell, n5] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n6 = grid_index_2D_to_1D_map[ix+1, iy-1]  # neighbour 6
        grid_laplacian[ith_cell, n6] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n7 = grid_index_2D_to_1D_map[ix, iy-1]  # neighbour 7
        grid_laplacian[ith_cell, n7] = -1
        neighbours += 1
    except KeyError:
        pass

    try:
        n8 = grid_index_2D_to_1D_map[ix-1, iy-1]  # neighbour 8
        grid_laplacian[ith_cell, n8] = -1
        neighbours += 1
    except KeyError:
        pass

    grid_laplacian[ith_cell, ith_cell] = neighbours


with open('kl11_voxel_grid.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for ith_voxel, voxel in enumerate(grid_cells):
        p1, p2, p3, p4 = voxel
        writer.writerow((ith_voxel, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y))


np.save(open('grid_laplacian.ndarray', 'wb'), csc_matrix(grid_laplacian))



