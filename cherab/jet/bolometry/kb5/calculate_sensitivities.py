
import time
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface
from raysect.primitive import import_obj

from cherab.jet.machine import import_jet_mesh
from cherab.jet.machine.cad_files import KB5V
from cherab.jet.bolometry import load_kb5_camera, load_kb5_inversion_grid


start_time = time.time()

# Load default inversion grid
grid = load_kb5_inversion_grid()

# Calculate KB5V camera sensitivities
world = World()
import_jet_mesh(world, material=AbsorbingSurface())
kb5v_collimator_mesh = import_obj(KB5V[0][0], scaling=0.001, parent=world, material=AbsorbingSurface())

kb5v = load_kb5_camera('KB5V', parent=world, inversion_grid=grid)
for detector in kb5v:
    print('calculating detector {}'.format(detector.detector_id))
    detector.calculate_sensitivity(grid)
kb5v.save("KB5V_camera.pickle")

print("run time - {:.2G}mins".format((time.time() - start_time) / 60))
