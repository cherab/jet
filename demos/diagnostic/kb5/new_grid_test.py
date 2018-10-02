
import time
import matplotlib.pyplot as plt
from raysect.primitive import import_obj
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface

from cherab.jet.machine import import_jet_mesh
from cherab.jet.machine.cad_files import KB5V, KB5H
from cherab.jet.bolometry import load_kb5_camera, load_kb5_inversion_grid


# Calculate KB5V camera sensitivities
kb5v_world = World()
inversion_grid = load_kb5_inversion_grid(parent=kb5v_world, name="KB5 inversion grid")
import_jet_mesh(kb5v_world, override_material=AbsorbingSurface())
kb5v_collimator_mesh = import_obj(KB5V[0][0], scaling=0.001, parent=kb5v_world, material=AbsorbingSurface())

kb5v = load_kb5_camera('KB5V', parent=kb5v_world)

kb5v_ch14 = kb5v['KB5V_CH14']
start_time = time.time()
sensitivities = kb5v_ch14.calculate_sensitivity(inversion_grid, ray_count=1000)
print("run time - {:.2G}mins".format((time.time() - start_time) / 60))

plt.ion()
inversion_grid.plot(voxel_values=sensitivities)
plt.show()


# start_time = time.time()
# for detector in kb5v:
#     print('calculating detector {}'.format(detector.detector_id))
#     detector.calculate_sensitivity(grid)
# kb5v.save("KB5V_camera.pickle")
#
# print("run time - {:.2G}mins".format((time.time() - start_time) / 60))


