
from raysect.core.math import Point3D
from cherab.tools.observers.bolometry import BolometerSlit, BolometerFoil, BolometerCamera

import numpy as np

foils = np.loadtxt('kb5v_foils.csv', delimiter=',')
slits = np.loadtxt('kb5v_slits.csv', delimiter=',')


kb5vertical = BolometerCamera(name="KB5V")

for i in range(32):

    slit_data = slits[i]
    slit_id = 'KB5V_CH{}_SLIT'.format(str(int(slit_data[0])))
    p1 = Point3D(slit_data[1], slit_data[2], slit_data[3])
    p2 = Point3D(slit_data[4], slit_data[5], slit_data[6])
    p3 = Point3D(slit_data[7], slit_data[8], slit_data[9])
    p4 = Point3D(slit_data[10], slit_data[11], slit_data[12])
    basis_x = p1.vector_to(p2).normalise()
    dx = p1.distance_to(p2)
    basis_y = p2.vector_to(p3).normalise()
    dy = p2.distance_to(p3)
    centre_point = Point3D((p1.x + p2.x + p3.x + p4.x)/4, (p1.y + p2.y + p3.y + p4.y)/4, (p1.z + p2.z + p3.z + p4.z)/4)
    slit = BolometerSlit(slit_id, centre_point, basis_x, dx, basis_y, dy)

    foil_data = foils[i]
    foil_id = 'KB5V_CH{}'.format(str(int(foil_data[0])))
    p1 = Point3D(foil_data[1], foil_data[2], foil_data[3])
    p2 = Point3D(foil_data[4], foil_data[5], foil_data[6])
    p3 = Point3D(foil_data[7], foil_data[8], foil_data[9])
    p4 = Point3D(foil_data[10], foil_data[11], foil_data[12])
    basis_x = p1.vector_to(p2).normalise()
    dx = p1.distance_to(p2)
    basis_y = p2.vector_to(p3).normalise()
    dy = p2.distance_to(p3)
    centre_point = Point3D((p1.x + p2.x + p3.x + p4.x)/4, (p1.y + p2.y + p3.y + p4.y)/4, (p1.z + p2.z + p3.z + p4.z)/4)

    # Shift backwards 3mm for all foils except those explicitely measured on back plate
    if i not in (25-1, 32-1):
        basis_z = basis_x.cross(basis_y).normalise()
        centre_point = centre_point - basis_z * 0.0031

    foil = BolometerFoil(foil_id, centre_point, basis_x, dx, basis_y, dy, slit)

    kb5vertical.add_foil_detector(foil)

kb5vertical.save('KB5V_camera.json')

