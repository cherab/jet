

from raysect.optical.observer import PowerPipeline2D, VectorCamera

from cherab.tools.observers import load_calcam_calibration


def load_kl11_camera(parent=None, pipelines=None):

    camera_config = load_calcam_calibration('/home/mcarr/cherab/cherab_jet/cherab/jet/cameras/kl11/KL11-E1DC_87516.nc')

    if not pipelines:
        power_unfiltered = PowerPipeline2D(display_unsaturated_fraction=0.96, name="Unfiltered Power (W)")
        power_unfiltered.display_update_time = 15
        pipelines = [power_unfiltered]

    pixels_shape, pixel_origins, pixel_directions = camera_config
    camera = VectorCamera(pixel_origins, pixel_directions, pipelines=pipelines, parent=parent)
    camera.spectral_bins = 15
    camera.pixel_samples = 1

    return camera
