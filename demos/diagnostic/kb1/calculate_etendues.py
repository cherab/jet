
import numpy as np

from raysect.optical import World
from raysect.core.math.sampler import TargettedHemisphereSampler, RectangleSampler3D
from raysect.core import Ray as CoreRay
from raysect.optical.material import NullMaterial

from cherab.jet.machine import import_jet_mesh
from cherab.jet.bolometry import load_kb1_camera

R_2_PI = 1 / (2 * np.pi)

world = World()

kb1 = load_kb1_camera(parent=world)

# JET vessel forms the KB1 aperture, so need to load this too
import_jet_mesh(world)


# We don't want to include ray hits with the bottom of the vessel in the
# etendue calculation. So we need to modify BolometerFoil.calculate_etendue
# for this special case
def calculate_etendue(self, ray_count=10000, batches=10):
    target = self.slit.target

    world = self.slit.root
    detector_transform = self.to_root()

    # generate bounding sphere and convert to local coordinate system
    sphere = target.bounding_sphere()
    spheres = [(sphere.centre.transform(self.to_local()), sphere.radius, 1.0)]
    # instance targetted pixel sampler
    targetted_sampler = TargettedHemisphereSampler(spheres)

    etendues = []
    for i in range(batches):

        # sample pixel origins
        point_sampler = RectangleSampler3D(width=self.x_width, height=self.y_width)
        origins = point_sampler(samples=ray_count)

        passed = 0.0
        for origin in origins:

            # obtain targetted vector sample
            direction, pdf = targetted_sampler(origin, pdf=True)
            path_weight = R_2_PI * direction.z/pdf

            origin = origin.transform(detector_transform)
            direction = direction.transform(detector_transform)

            while True:

                # Find the next intersection point of the ray with the world
                intersection = world.hit(CoreRay(origin, direction))

                if intersection is None or intersection.hit_point.transform(intersection.primitive_to_world).z < 0:
                    passed += 1 * path_weight
                    break

                elif isinstance(intersection.primitive.material, NullMaterial):
                    hit_point = intersection.hit_point.transform(intersection.primitive_to_world)
                    # apply a small displacement to avoid infinite self collisions due to numerics
                    ray_displacement = min(self.x_width, self.y_width) / 100
                    origin = hit_point + direction * ray_displacement
                    continue

                else:
                    break

        etendue_fraction = passed / ray_count

        etendues.append(self.sensitivity * etendue_fraction)

    etendue = np.mean(etendues)
    etendue_error = np.std(etendues)

    return etendue, etendue_error


kb1_etendues = []
for detector in kb1:
    etendue, etendue_error = calculate_etendue(detector, ray_count=1000000)
    print("Detector {}: etendue {:.4G} +- {:.3G} m^2 str".format(detector.name, etendue, etendue_error))
    kb1_etendues.append((etendue, etendue_error))
    np.save("kb1_etendue.npy", kb1_etendues)
