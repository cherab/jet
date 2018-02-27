
# Core and external imports
import numpy as np
import matplotlib.pyplot as plt
from raysect.core import Ray as CoreRay, Point3D, Vector3D
from raysect.optical import World, Ray
from raysect.optical.observer import PowerPipeline2D
from raysect.optical.material import AbsorbingSurface

# Cherab imports
from cherab.core.atomic import Line
from cherab.core.atomic.elements import deuterium
from cherab.core.model import ExcitationLine, RecombinationLine
from cherab.edge2d import load_edge2d_from_eproc
from cherab.openadas import OpenADAS
from cherab.jet.machine import import_jet_mesh
from cherab.jet.cameras.kl11 import load_kl11_camera


world = World()
import_jet_mesh(world)


# run1706184 jsimpson/edge2d/jet/85274/aug0717/seq#23  /home/jsimpson/cmg/catalog/edge2d/jet/85274/aug0717/seq#23
# run1706188 jsimpson/edge2d/jet/85274/aug0717/seq#27

edge2d_sim = load_edge2d_from_eproc('/home/jsimpson/cmg/catalog/edge2d/jet/85274/aug0717/seq#23/tran')
plasma = edge2d_sim.create_plasma(parent=world)
plasma.atomic_data = OpenADAS(permit_extrapolation=True)

# Pick emission models
d_alpha = Line(deuterium, 0, (3, 2))
plasma.models = [ExcitationLine(d_alpha), RecombinationLine(d_alpha)]

# plt.ion()
# Setup camera for interactive use...
power_unfiltered = PowerPipeline2D(display_unsaturated_fraction=0.96, name="Unfiltered Power (W)", display_progress=False)
power_unfiltered.display_update_time = 15

camera = load_kl11_camera(parent=world, pipelines=[power_unfiltered])
camera.pixel_samples = 150
camera.ray_max_depth = 3
camera.observe()

np.save('KL11_run1706184_reflecting_150', power_unfiltered.frame.mean)
power_unfiltered.save('KL11_run1706184_reflecting_150')
