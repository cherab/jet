import os
import numpy as np
from raysect.core import Point3D
from raysect.primitive import Mesh

from cherab.tools.observers.bolometry import (
    BolometerCamera,
    BolometerSlit,
    BolometerFoil,
)
from cherab.jet.machine import KB3H03, KB3H04


_DATA_PATH = os.path.split(__file__)[0]


def load_kb3_camera(camera_id, parent=None, override_material=None):

    if camera_id == "KB3H03":
        foils = np.loadtxt(os.path.join(_DATA_PATH, "kb3h03_foils.csv"), delimiter=",")
        slits = np.loadtxt(os.path.join(_DATA_PATH, "kb3h03_slits.csv"), delimiter=",")
        mesh_data = KB3H03[0]
    elif camera_id == "KB3H04":
        foils = np.loadtxt(os.path.join(_DATA_PATH, "kb3h04_foils.csv"), delimiter=",")
        slits = np.loadtxt(os.path.join(_DATA_PATH, "kb3h04_slits.csv"), delimiter=",")
        mesh_data = KB3H04[0]
    else:
        raise ValueError("Unrecognised bolometer camera_id '{}'.".format(camera_id))

    num_slits = slits.shape[0]
    num_foils = foils.shape[0]

    mesh_file = mesh_data[0]
    mesh_material = override_material or mesh_data[1]

    camera_geometry = Mesh.from_file(mesh_file)

    camera_geometry.name = "{} mesh geometry".format(camera_id)
    camera_geometry.material = mesh_material

    bolometer_camera = BolometerCamera(
        name=camera_id, parent=parent, camera_geometry=camera_geometry
    )

    slit_objects = {}
    for i in range(num_slits):
        slit_data = slits[i]
        slit_id = "{}_Slit_#{}".format(camera_id, str(int(slit_data[0])))
        p1 = Point3D(slit_data[1], slit_data[2], slit_data[3])
        p2 = Point3D(slit_data[4], slit_data[5], slit_data[6])
        p3 = Point3D(slit_data[7], slit_data[8], slit_data[9])
        p4 = Point3D(slit_data[10], slit_data[11], slit_data[12])
        basis_x = p1.vector_to(p2).normalise()
        dx = p1.distance_to(p2)
        basis_y = p2.vector_to(p3).normalise()
        dy = p2.distance_to(p3)
        centre_point = Point3D(
            (p1.x + p2.x + p3.x + p4.x) / 4,
            (p1.y + p2.y + p3.y + p4.y) / 4,
            (p1.z + p2.z + p3.z + p4.z) / 4,
        )
        slit_objects[slit_id] = BolometerSlit(
            slit_id, centre_point, basis_x, dx, basis_y, dy, parent=bolometer_camera
        )

    # kb3 channels are marged by letters, not numbers as in kb5 case
    num2name = {1: "A", 2: "B", 3: "C", 4: "D"}

    for i in range(num_foils):
        foil_data = foils[i]
        foil_id = "{}_CH{}_Foil".format(camera_id, num2name[i + 1])
        slit_id = "{}_Slit_#{}".format(camera_id, str(int(foil_data[1])))

        p1 = Point3D(foil_data[2], foil_data[3], foil_data[4])
        p2 = Point3D(foil_data[5], foil_data[6], foil_data[7])
        p3 = Point3D(foil_data[8], foil_data[9], foil_data[10])
        p4 = Point3D(foil_data[11], foil_data[12], foil_data[13])
        basis_x = p2.vector_to(
            p1
        ).normalise()  # switching orientation to ensure face orientation is correct
        dx = p1.distance_to(p2)
        basis_y = p2.vector_to(p3).normalise()
        dy = p2.distance_to(p3)
        centre_point = Point3D(
            (p1.x + p2.x + p3.x + p4.x) / 4,
            (p1.y + p2.y + p3.y + p4.y) / 4,
            (p1.z + p2.z + p3.z + p4.z) / 4,
        )

        foil = BolometerFoil(
            foil_id,
            centre_point,
            basis_x,
            dx,
            basis_y,
            dy,
            slit_objects[slit_id],
            parent=bolometer_camera,
        )

        bolometer_camera.add_foil_detector(foil)

    return bolometer_camera
