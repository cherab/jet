
import time
import numpy as np
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface
from raysect.core.workflow import MulticoreEngine

from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb5_camera, load_kb5_voxel_grid


world = World()
inversion_grid = load_kb5_voxel_grid(parent=world, name="KB5 inversion grid")
import_jet_mesh(world, override_material=AbsorbingSurface())

# Calculate KB5V camera sensitivities
kb5v = load_kb5_camera('KB5V', parent=world, override_material=AbsorbingSurface())
sensitivity_matrix = np.zeros((len(kb5v), inversion_grid.count))
for i, detector in enumerate(kb5v):
    detector.render_engine = MulticoreEngine(10)
    start_time = time.time()
    sensitivities = detector.calculate_sensitivity(inversion_grid, ray_count=10000)
    sensitivity_matrix[i, :] = sensitivities
    print("Traced detector '{}' with run time - {:.2G}mins".format(detector.name, (time.time() - start_time) / 60))
np.save("kb5v_sensitivities.npy", sensitivity_matrix)


# Calculate KB5H camera sensitivities
kb5h = load_kb5_camera('KB5H', parent=world, override_material=AbsorbingSurface())
sensitivity_matrix = np.zeros((len(kb5h), inversion_grid.count))
for i, detector in enumerate(kb5h):
    detector.render_engine = MulticoreEngine(10)
    start_time = time.time()
    sensitivities = detector.calculate_sensitivity(inversion_grid, ray_count=10000)
    sensitivity_matrix[i, :] = sensitivities
    print("Traced detector '{}' with run time - {:.2G}mins".format(detector.name, (time.time() - start_time) / 60))
np.save("kb5h_sensitivities.npy", sensitivity_matrix)
