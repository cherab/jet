
from math import sqrt
import matplotlib.pyplot as plt
from raysect.optical import World
from raysect.optical.material import AbsorbingSurface

from cherab.jet.machine import import_jet_mesh, plot_jet_wall_outline
from cherab.jet.bolometry import load_kb5_camera


# Calculate KB5V camera sensitivities
world = World()
import_jet_mesh(world, override_material=AbsorbingSurface())


plt.ion()
kb5v = load_kb5_camera('KB5V', parent=world, override_material=AbsorbingSurface())
for detector in kb5v:

    try:
        start, end, primitive = detector.trace_sightline()
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)
        print("Detector '{}' intersects with primitive '{}'.".format(detector.name, primitive.name))

    except RuntimeError:
        print("No intersection found for detector '{}'.".format(detector.name))
        start = detector.centre_point
        direction = detector.sightline_vector
        end = start + direction * 5
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)

    plt.plot([enx], [end.z], '.b')
    plt.plot([stx, enx], [start.z, end.z], 'k')

plot_jet_wall_outline()


kb5h = load_kb5_camera('KB5H', parent=world, override_material=AbsorbingSurface())
for detector in kb5h:

    try:
        start, end, primitive = detector.trace_sightline()
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)
        print("Detector '{}' intersects with primitive '{}'.".format(detector.name, primitive.name))

    except RuntimeError:
        print("No intersection found for detector '{}'.".format(detector.name))
        start = detector.centre_point
        direction = detector.sightline_vector
        end = start + direction * 5
        stx = sqrt(start.x**2 + start.y**2)
        enx = sqrt(end.x**2 + end.y**2)

    plt.plot([stx, enx], [start.z, end.z], 'k')

plot_jet_wall_outline()


plt.show()
