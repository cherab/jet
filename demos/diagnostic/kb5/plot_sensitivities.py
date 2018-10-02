
import numpy as np
import matplotlib.pyplot as plt

from cherab.jet.bolometry import load_kb5_inversion_grid, load_kb5_camera
from cherab.jet.machine import plot_jet_wall_outline

plt.ion()
inversion_grid = load_kb5_inversion_grid()

kb5v = load_kb5_camera('KB5V')
kb5v_sensitivities = np.load('kb5v_sensitivities.npy')
for i, detector in enumerate(kb5v):
    inversion_grid.plot(voxel_values=kb5v_sensitivities[i], title='{} sensitivities'.format(detector.name))
    plot_jet_wall_outline()
plt.show()
input("waiting...")
plt.close('all')


kb5h = load_kb5_camera('KB5H')
kb5h_sensitivities = np.load('kb5h_sensitivities.npy')
for i, detector in enumerate(kb5h):
    inversion_grid.plot(voxel_values=kb5h_sensitivities[i], title='{} sensitivities'.format(detector.name))
    plot_jet_wall_outline()
plt.show()
input("waiting...")
plt.close('all')
