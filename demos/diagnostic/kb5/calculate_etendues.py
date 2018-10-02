

from raysect.primitive import import_obj
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface

from cherab.jet.machine.cad_files import KB5V, KB5H
from cherab.jet.bolometry import load_kb5_camera


# Calculate KB5V camera sensitivities
world = World()
kb5v_collimator_mesh = import_obj(KB5V[0][0], scaling=0.001, name='kb5v_collimator',
                                  parent=world, material=AbsorbingSurface())
kb5h_collimator_mesh = import_obj(KB5H[0][0], scaling=0.001, name='kb5h_collimator',
                                  parent=world, material=AbsorbingSurface())


kb5v = load_kb5_camera('KB5V', parent=world)
for detector in kb5v:

    etendue, etendue_error = detector.calculate_etendue(ray_count=400000)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))


kb5h = load_kb5_camera('KB5H', parent=world)
for detector in kb5h:

    etendue, etendue_error = detector.calculate_etendue(ray_count=400000)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))
