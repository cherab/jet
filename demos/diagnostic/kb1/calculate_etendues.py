
import numpy as np

from raysect.optical import World
from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb1_camera


world = World()

kb1 = load_kb1_camera(parent=world)

# JET vessel forms the KB1 aperture, so need to load this too
import_jet_mesh(world)


kb1_etendues = []
for detector in kb1:
    # Don't count ray-primitive intersections further than 2 metres from the foil:
    # these occur when the ray hits the bottom of the vessel
    etendue, etendue_error = detector.calculate_etendue(ray_count=10000, max_distance=2)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))
    kb1_etendues.append((etendue, etendue_error))
np.save("kb1_etendue.npy", kb1_etendues)
