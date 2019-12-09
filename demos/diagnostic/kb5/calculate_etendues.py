import numpy as np

from raysect.optical import World
from raysect.optical.material import AbsorbingSurface

from cherab.jet.bolometry import load_kb5_camera


world = World()

kb5v = load_kb5_camera('KB5V', parent=world, override_material=AbsorbingSurface())
kb5v_etendues = []
for detector in kb5v:
    etendue, etendue_error = detector.calculate_etendue(ray_count=400000)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))
    kb5v_etendues.append((etendue, etendue_error))
np.save("kb5v_etendue.npy", kb5v_etendues)


kb5h = load_kb5_camera('KB5H', parent=world, override_material=AbsorbingSurface())
kb5h_etendues = []
for detector in kb5h:
    etendue, etendue_error = detector.calculate_etendue(ray_count=400000)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))
    kb5h_etendues.append((etendue, etendue_error))
np.save("kb5h_etendue.npy", kb5h_etendues)
