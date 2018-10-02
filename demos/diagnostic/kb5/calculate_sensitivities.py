
import time
import numpy as np
from raysect.primitive import import_obj
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface
from raysect.core.workflow import MulticoreEngine

from cherab.jet.machine import import_jet_mesh
from cherab.jet.machine.cad_files import KB5V, KB5H
from cherab.jet.bolometry import load_kb5_camera, load_kb5_inversion_grid


world = World()
inversion_grid = load_kb5_inversion_grid(parent=world, name="KB5 inversion grid")
import_jet_mesh(world, override_material=AbsorbingSurface())
kb5v_collimator_mesh = import_obj(KB5V[0][0], scaling=0.001, parent=world, material=AbsorbingSurface())
kb5h_collimator_mesh = import_obj(KB5H[0][0], scaling=0.001, parent=world, material=AbsorbingSurface())


# Calculate KB5V camera sensitivities
kb5v = load_kb5_camera('KB5V', parent=world)
kb5v.render_engine = MulticoreEngine(10)
sensitivity_matrix = np.zeros((len(kb5v), inversion_grid.count))
for i, detector in enumerate(kb5v):
    start_time = time.time()
    sensitivities = detector.calculate_sensitivity(inversion_grid, ray_count=10000)
    sensitivity_matrix[i, :] = sensitivities
    print("Traced detector '{}' with run time - {:.2G}mins".format(detector.name, (time.time() - start_time) / 60))
np.save("kb5v_sensitivities.npy", sensitivity_matrix)


# Calculate KB5H camera sensitivities
kb5h = load_kb5_camera('KB5H', parent=world)
kb5h.render_engine = MulticoreEngine(10)
sensitivity_matrix = np.zeros((len(kb5h), inversion_grid.count))
for i, detector in enumerate(kb5h):
    start_time = time.time()
    sensitivities = detector.calculate_sensitivity(inversion_grid, ray_count=10000)
    sensitivity_matrix[i, :] = sensitivities
    print("Traced detector '{}' with run time - {:.2G}mins".format(detector.name, (time.time() - start_time) / 60))
np.save("kb5h_sensitivities.npy", sensitivity_matrix)
