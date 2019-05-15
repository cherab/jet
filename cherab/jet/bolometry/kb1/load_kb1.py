
import os
import pickle
import textwrap
from raysect.core import Point2D, Point3D, Vector3D, translate, rotate_z, rotate_basis

from cherab.tools.observers.bolometry import BolometerCamera, BolometerSlit, BolometerFoil
from cherab.tools.inversions import ToroidalVoxelGrid


_DATA_PATH = os.path.split(__file__)[0]


def load_kb1_camera(parent=None):

    camera_id = 'KB1'

    # Transforms, read from KB1 CAD model for INDIVIDUAL_BOLOMETER_ASSEMBLY
    # Note that the rotation angle is positive when Axis is the Z axis, and
    # negative when Axis is the -Z axis
    camera_transforms = [
        translate(-1.73116, 2.59086, 3.31650) * rotate_z(123.75),
        translate(-3.05613, 0.60790, 3.31650) * rotate_z(168.75),
        translate(1.73116, -2.59086, 3.31650) * rotate_z(-56.25),
        translate(3.05613, -0.60790, 3.31650) * rotate_z(-11.25),
    ]
    # Transform for INDIVIDUAL_BOLOMETER_ASSEMBLY/SINGLE_BOLOMETER_ASSEMBLY/FOIL 1
    # in CAD model
    foil_camera_transform = translate(0, 0, 18.70e-3)
    # Foils point downwards towards the plasma
    foil_orientation_transform = rotate_basis(Vector3D(0, 0, -1), Vector3D(0, 1, 0))
    # Dimensions read from edge to edge (and adjacent vertices defining rounded corners) on
    # INDIVIDUAL_BOLOMETER_ASSEMBLY/SINGLE_BOLOMETER_ASSEMBLY/FOIL SUPPORT 1,
    # edges (and vertices) closest to the foil
    foil_width = 11e-3
    foil_height = 11e-3
    foil_curvature_radius = 1e-3

    # KB1 does not really have a slit, per-se. The vessel functions as the
    # aperture. To ensure a sufficiently displaced bounding sphere for the
    # TargettedPixel, we'll put a dummy slit at the exit of the port through
    # which the camera views. Note that with the camera transform defined above,
    # the y axis is in the toroidal direction and the x axis in the inward
    # radial direction.
    #
    # The foil is not centred on the centre of the port. To measure the
    # displacement, the centre of the port was read from the CAD model for
    # KB1-1, then the vector from the foil centre to the centre of the port exit
    # for this channel was calculated in the foil's local coordinate system.
    foil_slit_transform = translate(-0.05025, 0, 1.38658)
    slit_width = 0.25  # slightly larger than widest point of port (~225 mm)
    slit_height = 0.09  # sligtly larger than length of port (~73.84 mm)

    num_slits = len(camera_transforms)
    num_foils = len(camera_transforms)

    bolometer_camera = BolometerCamera(name=camera_id, parent=parent)

    slit_objects = {}
    for i in range(num_slits):
        slit_id = '{}_Slit_#{}'.format(camera_id, i + 1)
        slit_transform = (camera_transforms[i]
                          * foil_orientation_transform
                          * foil_slit_transform
                          * foil_camera_transform)
        centre_point = Point3D(0, 0, 0).transform(slit_transform)
        basis_x = Vector3D(1, 0, 0).transform(slit_transform)
        basis_y = Vector3D(0, 1, 0).transform(slit_transform)
        dx = slit_width
        dy = slit_height
        slit_objects[slit_id] = BolometerSlit(
            slit_id, centre_point, basis_x, dx, basis_y, dy, csg_aperture=True,
            parent=bolometer_camera)

    for i in range(num_foils):
        foil_id = '{}_CH{}_Foil'.format(camera_id, i + 1)
        slit_id = '{}_Slit_#{}'.format(camera_id, i+ 1)
        foil_transform = (camera_transforms[i]
                          * foil_orientation_transform
                          * foil_camera_transform)
        centre_point = Point3D(0, 0, 0).transform(foil_transform)
        basis_x = Vector3D(1, 0, 0).transform(foil_transform)
        basis_y = Vector3D(0, 1, 0).transform(foil_transform)
        dx = foil_width
        dy = foil_height
        rc = foil_curvature_radius
        foil = BolometerFoil(
            foil_id, centre_point, basis_x, dx, basis_y, dy, slit_objects[slit_id],
            curvature_radius=rc, parent=bolometer_camera)

        bolometer_camera.add_foil_detector(foil)

    return bolometer_camera


def _read_grid_pickle():
    grid_file_name = "kb1_voxel_grid.pickle"
    voxel_grid_file = os.path.join(_DATA_PATH, grid_file_name)

    try:
        with open(voxel_grid_file, 'rb') as fh:
            grid_description = pickle.load(fh)
    except FileNotFoundError:
        message = textwrap.dedent(
            """
            {}
            not found: please run the grid_generation.py script in
            the KB1 demos directory to generate the default grid, or
            produce a new grid in the same file format with the same
            path."""
            .format(voxel_grid_file)
        )
        raise FileNotFoundError(message)
    return grid_description


def load_kb1_voxel_grid(parent=None, name=None):

    grid_description = _read_grid_pickle()

    voxel_coordinates = []
    for voxel in grid_description['voxels']:
        v1 = Point2D(voxel[0][0], voxel[0][1])
        v2 = Point2D(voxel[1][0], voxel[1][1])
        v3 = Point2D(voxel[2][0], voxel[2][1])
        v4 = Point2D(voxel[3][0], voxel[3][1])
        voxel_coordinates.append((v1, v2, v3, v4))

    voxel_grid = ToroidalVoxelGrid(voxel_coordinates, parent=parent, name=name,
                                   primitive_type="csg")

    return voxel_grid


def load_kb1_grid_extras():
    """
    Return extra information about the grid.

    This includes the 1D<->2D mappings, but not the voxel coordinates.
    Use load_kb1_voxel_grid for that.
    """
    grid_description = _read_grid_pickle()
    grid_description.pop('voxels')
    return grid_description
