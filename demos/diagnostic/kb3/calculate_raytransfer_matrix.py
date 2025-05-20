import numpy as np

import matplotlib.pyplot as plt

from raysect.optical import World, AbsorbingSurface, translate

from cherab.tools.raytransfer import RayTransferCylinder, RayTransferPipeline0D

from cherab.jet.bolometry import load_kb3_camera
from cherab.jet.machine import import_jet_mesh, firstwall

world = World()
import_jet_mesh(world, override_material=AbsorbingSurface(), verbose=False)

# load the cameras
kb3h03 = load_kb3_camera("KB3H03", parent=world, override_material=AbsorbingSurface())
kb3h04 = load_kb3_camera("KB3H04", parent=world, override_material=AbsorbingSurface())

# configure the raytransfer cylinder, perform observation
radius_outer = 4.0 # the outer radius of the contribution matrix grid
radius_inner = 1.8 # the inner radius of the contribution matrix grid
height = 4.0 # the height of the contribution matrix grid
n_radius = 110 # the number of radial bins
n_height = 200 # the number of height bins
z_offset = -1.9 # the minimum z-coordinate of the contribution matrix grid

raytransfer_cylinder = RayTransferCylinder(
    radius_outer=radius_outer,
    radius_inner=radius_inner,
    height=height,
    n_radius=n_radius,
    n_height=n_height,
)
raytransfer_cylinder.transform = translate(0, 0, z_offset)
raytransfer_cylinder.parent = world

for channel in kb3h03:
    channel.spectral_bins = raytransfer_cylinder.bins
    channel.min_wavelength = 600.0
    channel.max_wavelength = 610.0
    channel.pipelines = [RayTransferPipeline0D(kind="power")]
    channel.observe()

for channel in kb3h04:
    channel.spectral_bins = raytransfer_cylinder.bins
    channel.min_wavelength = 600.0
    channel.max_wavelength = 610.0
    channel.pipelines = [RayTransferPipeline0D(kind="power")]
    channel.observe()

# reshape the contribution data into contribution matrices
contrib_kb3h03 = np.concatenate(
    [channel.pipelines[0].matrix[raytransfer_cylinder.voxel_map.T] for channel in kb3h03], axis=1
)
contrib_kb3h04 = np.concatenate(
    [channel.pipelines[0].matrix[raytransfer_cylinder.voxel_map.T] for channel in kb3h04], axis=1
)

# plot results
raytransfer_material = raytransfer_cylinder.material

r = (raytransfer_material.rmin + 0.5 * raytransfer_material.dr) + raytransfer_material.dr * np.arange(raytransfer_material.grid_shape[0])
z = (z_offset + 0.5 * raytransfer_material.dz) + raytransfer_material.dz * np.arange(raytransfer_material.grid_shape[2])

jet_firstwall = firstwall()

_, ax = plt.subplots(1, 2,constrained_layout=True, figsize=(12, 5))
ax[0].pcolormesh(r, z, contrib_kb3h03.sum(axis=1))
ax[0].plot(jet_firstwall[:, 0], jet_firstwall[:, 1], 'w-')
ax[0].set_ylim(None, -1.0)
ax[0].set_xlim(2.0, 3.25)
ax[0].set_xlabel(r"$R$ [m]")
ax[0].set_ylabel(r"$Z$ [m]")
ax[0].set_aspect('equal')
ax[0].set_title("KB3H03")
ax[0].tick_params(axis='both', which='major', labelsize=14)
ax[0].xaxis.label.set_size(14)
ax[0].yaxis.label.set_size(14)

ax[1].pcolormesh(r, z, contrib_kb3h04.sum(axis=1))
ax[1].plot(jet_firstwall[:, 0], jet_firstwall[:, 1], 'w-')
ax[1].set_ylim(None, -1.0)
ax[1].set_xlim(2.0, 3.25)
ax[1].set_aspect('equal')
ax[1].set_title("KB3H04")
ax[1].set_xlabel(r"$R$ [m]")
ax[1].set_ylabel(r"$Z$ [m]")
ax[1].tick_params(axis='both', which='major', labelsize=14)
ax[1].xaxis.label.set_size(14) 
ax[1].yaxis.label.set_size(14)

plt.show()
