
import time
import numpy as np
import matplotlib.pyplot as plt

from raysect.core.math.function.function2d import PythonFunction2D
from raysect.optical import World, Spectrum, Point3D, Vector3D

from cherab.core.atomic import Line
from cherab.core.atomic.elements import deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.edge2d import load_edge2d_from_eproc
from cherab.openadas import OpenADAS
from cherab.tools.observers import emissivity_grid_from_function, EmissivityGrid
from cherab.tools.inversions import invert_sart
from cherab.jet.cameras.kl11 import load_kl11_inversion_grid, load_kl11_sensitivity_matrix


X_VECTOR = Vector3D(1, 0, 0)


class DAlphaEmissionFunction:

    def __init__(self, excit, recom, spectral_settings):
        self.excit = excit
        self.recom = recom
        self.spectral_settings = spectral_settings

    def __call__(self, x, z):

        point = Point3D(x, 0, z)
        spectrum = Spectrum(self.spectral_settings[0], self.spectral_settings[1], self.spectral_settings[2])
        spectrum = self.excit.emission(point, X_VECTOR, spectrum)
        spectrum = self.recom.emission(point, X_VECTOR, spectrum)

        return spectrum.total()


world = World()

edge2d_sim = load_edge2d_from_eproc('/home/jsimpson/cmg/catalog/edge2d/jet/85274/aug0717/seq#23/tran')
plasma = edge2d_sim.create_plasma(parent=world)
plasma.atomic_data = OpenADAS(permit_extrapolation=True)

# Pick emission models
d_alpha = Line(deuterium, 0, (3, 2))
d_alpha_exc = ExcitationLine(d_alpha)
d_alpha_recom = RecombinationLine(d_alpha)
plasma.models = [d_alpha_exc, d_alpha_recom]
emission_function = PythonFunction2D(DAlphaEmissionFunction(d_alpha_exc, d_alpha_recom, (650, 660, 1)))


inversion_grid = load_kl11_inversion_grid()
emission_grid = emissivity_grid_from_function(inversion_grid, emission_function)
emission_grid.plot()
plt.xlim(2.3, 3.0)
plt.ylim(-1.8, -1.2)


time_a = time.time()
sensitivity = load_kl11_sensitivity_matrix()
print('Time to load sensitivity matrix => ', (time.time() - time_a) / 60)
forward_image = np.matmul(sensitivity, emission_grid.emissivities)

plt.figure()
plt.imshow(forward_image.reshape((1000, 1000)))
plt.title('Forward modelled image')


time_a = time.time()
inverted_emission, conv = invert_sart(sensitivity, forward_image, max_iterations=100, debug=True)
print('Time to load sensitivity matrix => ', (time.time() - time_a) / 60)

inverted_emission = EmissivityGrid(inversion_grid, emissivities=inverted_emission)
inverted_emission.plot("Inverted emission profile")

plt.show()

