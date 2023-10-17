import numpy as np

from raysect.optical import World, Point3D
from raysect.optical.material.absorber import AbsorbingSurface

from cherab.jet.machine import import_jet_mesh, firstwall
from cherab.jet.spectroscopy.kt3 import kt3_from_sal
from cherab.jet.spectroscopy.kt3.kt3 import calculate_spot_position_sightline

import matplotlib.pyplot as plt

#select shot number and time
pulse_number = 96910
pulse_time = 56.0
world = World()

machine_components = import_jet_mesh(world, override_material=AbsorbingSurface(), verbose=False)

# create kt3 diagnostic models with spot position corrections
kt3a_corrected = kt3_from_sal("kt3a", pulse_number, parent=world, pulse_time=pulse_time)
kt3b_corrected = kt3_from_sal("kt3b", pulse_number, parent=world, pulse_time=pulse_time)

# create kt3 diagnostic models without spot shift corrrection
kt3a_nocorrection = kt3_from_sal("kt3a", pulse_number, parent=world, spot_position_correction=False)
kt3b_nocorrection = kt3_from_sal("kt3b", pulse_number, parent=world, spot_position_correction=False)

#initialise arrays to save spot positions to, array([sightline, [x, y, z], [origin, inner, center, outer]])
kt3a_corrected_spots = np.zeros((len(kt3a_corrected.sight_lines), 3, 4))
kt3b_corrected_spots = np.zeros((len(kt3b_corrected.sight_lines), 3, 4))
kt3a_nocorrection_spots = np.zeros((len(kt3a_nocorrection.sight_lines), 3, 4))
kt3b_nocorrection_spots = np.zeros((len(kt3b_nocorrection.sight_lines), 3, 4))

# get sightline trajectories, array
list_diagnostics = [ kt3a_corrected, kt3b_corrected,
                    kt3a_nocorrection, kt3b_nocorrection]
list_arrays = [ kt3a_corrected_spots, kt3b_corrected_spots,
               kt3a_nocorrection_spots, kt3b_nocorrection_spots]
for i, (diagnostic, arr) in enumerate(zip(list_diagnostics, list_arrays)):
    for i, sight_line in enumerate(diagnostic.sight_lines):
        origin = Point3D(0, 0, 0).transform(sight_line.to_root())
        hit_inner, hit_center, hit_outer = calculate_spot_position_sightline(sight_line)

        arr[i, :, 0] = (origin.x, origin.y, origin.z)
        arr[i, :, 1] = hit_inner
        arr[i, :, 2] = hit_center
        arr[i, :, 3] = hit_outer

# get vessel outline
outline = firstwall(pulse_number)

# plot kt3a/b sightlines of the corrected case with blocking avoidance
_, ax = plt.subplots(figsize=(10, 15))

r_origin = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C0-")

r_origin = np.sqrt(np.square(kt3b_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3b_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3b_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3b_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C1-")

ax.plot(outline[:, 0], outline[:, 1], "k")
ax.set_aspect(1)
# populate legend
ax.plot([], [], "C0", label="KT3A")
ax.plot([], [], "C1", label="KT3B")
ax.set_title("KT3A/B - corrected sight-lines")
ax.legend()

# plot kt3a/b sightlines of the corrected case
_, ax = plt.subplots(figsize=(10, 15))

r_origin = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C0-")

r_origin = np.sqrt(np.square(kt3b_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3b_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3b_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3b_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C1-")

ax.plot(outline[:, 0], outline[:, 1], "k")
ax.plot([], [], "C0", label="KT3A") # add a single label per spectromter
ax.plot([], [], "C1", label="KT3B") # add a single label per spectromter
ax.legend()
ax.set_title("KT3A/B - corrected sight-lines detail")
ax.set_xlim(2.3, 3.0)
ax.set_ylim(-1.8, -1.6)
ax.set_aspect(1)

# plot kt3a sightlines corrected/not corrected
_, ax = plt.subplots(figsize=(10, 15))

r_origin = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C0-")

r_origin = np.sqrt(np.square(kt3a_nocorrection_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_nocorrection_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_nocorrection_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_nocorrection_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C1-")

ax.plot(outline[:, 0], outline[:, 1], "k")
ax.plot([], [], "C0", label="Corrected") # add a single label per spectromter
ax.plot([], [], "C1", label="No Correction") # add a single label per spectromter
ax.legend()
ax.set_title("KT3A - Spot position correction effect")
ax.set_aspect(1)

# plot kt3a sightlines corrected/not corrected
_, ax = plt.subplots(figsize=(10, 15))

r_origin = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_corrected_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_corrected_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_corrected_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C0-")

r_origin = np.sqrt(np.square(kt3a_nocorrection_spots[:, 0:2, 0]).sum(axis=1))
z_origin = kt3a_nocorrection_spots[:, -1, 0]
r_spot = np.sqrt(np.square(kt3a_nocorrection_spots[:, 0:2, 2]).sum(axis=1))
z_spot = kt3a_nocorrection_spots[:, -1, 2]
ax.plot([r_origin, r_spot], [z_origin, z_spot], "C1-")

ax.plot(outline[:, 0], outline[:, 1], "k")
ax.plot([], [], "C0", label="Corrected") # add a single label per spectromter
ax.plot([], [], "C1", label="No Correction") # add a single label per spectromter
ax.legend()
ax.set_title("KT3A - Spot position correction effect detail")
ax.set_xlim(2.3, 3.0)
ax.set_ylim(-1.8, -1.6)
ax.set_aspect(1)

