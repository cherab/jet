
import matplotlib.pyplot as plt

from cherab.jet.bolometry import load_kb5_inversion_grid, load_kb5_camera
from cherab.jet.machine import plot_jet_wall_outline


def plot_detector(detector):
    detector.los_radiance_sensitivity.plot()
    plot_jet_wall_outline()
    detector.volume_radiance_sensitivity.plot()
    plot_jet_wall_outline()


inversion_grid = load_kb5_inversion_grid()

kb5v = load_kb5_camera('KB5V', inversion_grid=inversion_grid)
for detector in kb5v:
    plot_detector(detector)
plt.show()
input("waiting...")
plt.close('all')


kb5h = load_kb5_camera('KB5H', inversion_grid=inversion_grid)
for detector in kb5h:
    plot_detector(detector)
plt.show()
input("waiting...")
plt.close('all')
