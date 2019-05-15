
import csv
import numpy as np
import matplotlib.pyplot as plt
from raysect.core import Point2D
from scipy.sparse import csc_matrix

from cherab.tools.inversions import ToroidalVoxelGrid
from cherab.jet.machine import get_jet_wall_mask, plot_jet_wall_outline


wall_mask = get_jet_wall_mask()

main_chamber_resolution = 0.03
main_chamber_xrange = (1.84, 3.88)
main_chamber_yrange = (-1.2, 2.0)

div_resolution = 0.01
div_xrange = (1.84, 3.88)
div_yrange = (-1.8, -1.2)


def make_grid_segment(grid_xrange, grid_yrange, grid_resolution):

    nx = int(((grid_xrange[1] - grid_xrange[0]) / grid_resolution))
    ny = int(((grid_yrange[1] - grid_yrange[0]) / grid_resolution))

    xpoints = np.linspace(grid_xrange[0], grid_xrange[1], num=nx)
    ypoints = np.linspace(grid_yrange[0], grid_yrange[1], num=ny)
    bool_mask = np.empty((nx, ny), dtype=bool)

    unwrapped_cell_index = 0
    grid_voxels = []
    grid_index_2D_to_1D_map = {}
    grid_index_1D_to_2D_map = {}
    for ix in range(nx-1):
        print("{:.3G} % complete".format(ix / (nx-1) * 100))
        for jy in range(ny-1):

            p1 = Point2D(xpoints[ix], ypoints[jy])
            p2 = Point2D(xpoints[ix], ypoints[jy+1])
            p3 = Point2D(xpoints[ix+1], ypoints[jy+1])
            p4 = Point2D(xpoints[ix+1], ypoints[jy])

            if wall_mask(*p1) or wall_mask(*p2) or wall_mask(*p3) or wall_mask(*p4):
                grid_voxels.append((p1, p2, p3, p4))
                bool_mask[ix, jy] = True
                grid_index_2D_to_1D_map[(ix, jy)] = unwrapped_cell_index
                grid_index_1D_to_2D_map[unwrapped_cell_index] = (ix, jy)
                unwrapped_cell_index += 1
            else:
                bool_mask[ix, jy] = False

    num_voxels = len(grid_voxels)

    grid_laplacian = np.zeros((num_voxels, num_voxels))
    for ith_cell in range(num_voxels):

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

    return grid_voxels, grid_laplacian


div_voxels, div_laplacian = make_grid_segment(div_xrange, div_yrange, div_resolution)
main_chamber_voxels, main_chamber_laplacian = make_grid_segment(main_chamber_xrange, main_chamber_yrange, main_chamber_resolution)

num_div_voxels = len(div_voxels)
num_main_chamber_voxels = len(main_chamber_voxels)
total_num_voxels = num_div_voxels + num_main_chamber_voxels

overall_voxels = div_voxels + main_chamber_voxels
overall_laplacian = np.zeros((total_num_voxels, total_num_voxels))
overall_laplacian[0:num_div_voxels, 0:num_div_voxels] = div_laplacian[:, :]
overall_laplacian[num_div_voxels::, num_div_voxels::] = main_chamber_laplacian[:, :]


plt.ion()
kl11_grid = ToroidalVoxelGrid(overall_voxels, 'JET KL11 grid')
kl11_grid.plot()
plot_jet_wall_outline()

kl11_grid.plot(voxel_values=overall_laplacian[int(num_div_voxels/2), :])
plot_jet_wall_outline()

kl11_grid.plot(voxel_values=overall_laplacian[int(num_div_voxels+num_main_chamber_voxels/2), :])
plot_jet_wall_outline()


with open('kl11_voxel_grid.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for ith_voxel, voxel in enumerate(overall_voxels):
        p1, p2, p3, p4 = voxel
        writer.writerow((ith_voxel, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y))

np.savez_compressed('grid_laplacian', grid_laplacian=overall_laplacian)
