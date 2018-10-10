
from math import sqrt
import matplotlib.pyplot as plt
from raysect.primitive import import_obj
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface

from cherab.jet.machine import import_jet_mesh, plot_jet_wall_outline
from cherab.jet.bolometry import load_kb1_camera


# Calculate KB5V camera sensitivities
world = World()
import_jet_mesh(world, override_material=AbsorbingSurface())

plt.ion()
kb1 = load_kb1_camera(parent=world)
for detector in kb1:

    try:
        start, end, primitive = detector.trace_sightline()
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)
        print("Detector '{}' intersects with primitive '{}'.".format(detector.name, primitive.name))

    except RuntimeError:
        print("No intersection found for detector '{}'.".format(detector.name))
        start = detector.centre_point
        direction = detector.sightline_vector.normalise()
        end = start + direction * 5
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)

    plt.plot([enx], [end.z], '.b')
    plt.plot([stx, enx], [start.z, end.z], 'k')

plot_jet_wall_outline()

plt.show()
