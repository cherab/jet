
import os
import numpy as np
import pickle
from raysect.core import Point2D, Point3D, Vector3D

from cherab.tools.observers.bolometry import BolometerCamera, BolometerSlit, BolometerFoil
from cherab.tools.inversions.voxels import ToroidalVoxelGrid


_DATA_PATH = os.path.split(__file__)[0]


def load_kb5_camera(camera_id, parent=None):

    if camera_id == 'KB5V':
        foils = np.loadtxt(os.path.join(_DATA_PATH, 'kb5v_foils.csv'), delimiter=',')
        slits = np.loadtxt(os.path.join(_DATA_PATH, 'kb5v_slits.csv'), delimiter=',')
    elif camera_id == 'KB5H':
        foils = np.loadtxt(os.path.join(_DATA_PATH, 'kb5h_foils.csv'), delimiter=',')
        slits = np.loadtxt(os.path.join(_DATA_PATH, 'kb5h_slits.csv'), delimiter=',')
    else:
        raise ValueError("Unrecognised bolometer camera_id '{}'.".format(camera_id))

    num_slits = slits.shape[0]
    num_foils = foils.shape[0]

    bolometer_camera = BolometerCamera(name=camera_id, parent=parent)

    slit_objects = {}
    for i in range(num_slits):
        slit_data = slits[i]
        slit_id = '{}_Slit_#{}'.format(camera_id, str(int(slit_data[0])))
        p1 = Point3D(slit_data[1], slit_data[2], slit_data[3])
        p2 = Point3D(slit_data[4], slit_data[5], slit_data[6])
        p3 = Point3D(slit_data[7], slit_data[8], slit_data[9])
        p4 = Point3D(slit_data[10], slit_data[11], slit_data[12])
        basis_x = p1.vector_to(p2).normalise()
        dx = p1.distance_to(p2)
        basis_y = p2.vector_to(p3).normalise()
        dy = p2.distance_to(p3)
        centre_point = Point3D((p1.x + p2.x + p3.x + p4.x)/4, (p1.y + p2.y + p3.y + p4.y)/4, (p1.z + p2.z + p3.z + p4.z)/4)
        slit_objects[slit_id] = BolometerSlit(slit_id, centre_point, basis_x, dx, basis_y, dy, parent=bolometer_camera)

    for i in range(num_foils):
        foil_data = foils[i]
        foil_id = '{}_CH{}_Foil'.format(camera_id, str(int(foil_data[0])))
        slit_id = '{}_Slit_#{}'.format(camera_id, str(int(foil_data[1])))

        p1 = Point3D(foil_data[2], foil_data[3], foil_data[4])
        p2 = Point3D(foil_data[5], foil_data[6], foil_data[7])
        p3 = Point3D(foil_data[8], foil_data[9], foil_data[10])
        p4 = Point3D(foil_data[11], foil_data[12], foil_data[13])
        basis_x = p2.vector_to(p1).normalise()  # switching orientation to ensure face orientation is correct
        dx = p1.distance_to(p2)
        basis_y = p2.vector_to(p3).normalise()
        dy = p2.distance_to(p3)
        centre_point = Point3D((p1.x + p2.x + p3.x + p4.x)/4, (p1.y + p2.y + p3.y + p4.y)/4, (p1.z + p2.z + p3.z + p4.z)/4)

        # Shift backwards 3mm for all foils except those explicitly measured on back plate
        if camera_id == "KB5V":
            if i not in (9-1, 25-1, 32-1):
                basis_z = basis_x.cross(basis_y).normalise()
                centre_point = centre_point - basis_z * 0.0032
            # if i == 9 - 1:
            #     centre_point = centre_point + basis_x * 0.001
            if i == 31-1:
                centre_point = centre_point - basis_x * 0.001


        # print()
        # print(slit_objects.keys())
        # print(slit_id)
        # print()
        foil = BolometerFoil(foil_id, centre_point, basis_x, dx, basis_y, dy, slit_objects[slit_id], parent=bolometer_camera)

        bolometer_camera.add_foil_detector(foil)

    return bolometer_camera


def load_kb5_inversion_grid(parent=None, name=None):

    old_grid = load_inversion_grid(os.path.join(_DATA_PATH, "kb5_inversion_grid.json"))

    cell_data = old_grid.cell_data

    cell_coordinates = []
    for cell_id in range(cell_data.shape[0]):

        p1 = Point2D(cell_data[cell_id, 0, 0], cell_data[cell_id, 0, 1])
        p2 = Point2D(cell_data[cell_id, 1, 0], cell_data[cell_id, 1, 1])
        p3 = Point2D(cell_data[cell_id, 2, 0], cell_data[cell_id, 2, 1])
        p4 = Point2D(cell_data[cell_id, 3, 0], cell_data[cell_id, 3, 1])
        cell_coordinates.append((p1, p2, p3, p4))

    new_grid = ToroidalVoxelGrid(cell_coordinates, parent=parent, name=name)

    return new_grid
