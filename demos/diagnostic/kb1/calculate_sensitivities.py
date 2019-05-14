
import time
import os
import numpy as np
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface
from raysect.core.workflow import MulticoreEngine

from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb1_camera, load_kb1_voxel_grid


NCORES = int(os.environ.get("NSLOTS", 4))


world = World()
voxel_grid = load_kb1_voxel_grid(parent=world, name="KB1 voxel grid")
import_jet_mesh(world, override_material=AbsorbingSurface())

# Calculate KB1 camera sensitivities
kb1 = load_kb1_camera(parent=world)
sensitivity_matrix = np.zeros((len(kb1), voxel_grid.count))
for i, detector in enumerate(kb1):
    start_time = time.time()
    print("Calculating detector '{}'...".format(detector.name))
    detector.render_engine = MulticoreEngine(NCORES)
    sensitivities = detector.calculate_sensitivity(voxel_grid, ray_count=1000000)
    sensitivity_matrix[i, :] = sensitivities
    print("Traced detector '{}' with run time - {:.2G}mins".format(detector.name, (time.time() - start_time) / 60))
np.save("kb1_sensitivities.npy", sensitivity_matrix)
