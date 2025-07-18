

from raysect.optical.observer import PowerPipeline2D, VectorCamera

from cherab.tools.observers import load_calcam_calibration


def load_kl1_camera(parent=None, pipelines=None, stride=1,
                    calibration_file = '/home/mcarr/cherab/cherab_jet/cherab/jet/cameras/kl1/kl1-e4wc-sightlines.nc'):
    """
    Load Camera calibration fron an *.nc file.

    :param parent: parent of the camera observer
    :param pipeline: camera pipelines
    :param stride: Binning parameter, only every nth pixel from the calibration is used
    """

    camera_config = load_calcam_calibration(calibration_file)

    if not pipelines:
        power_unfiltered = PowerPipeline2D(display_unsaturated_fraction=0.96, name="Unfiltered Power (W)")
        power_unfiltered.display_update_time = 15
        pipelines = [power_unfiltered]

    pixels_shape, pixel_origins, pixel_directions = camera_config
    camera = VectorCamera(pixel_origins[::stride, ::stride], pixel_directions[::stride, ::stride], pipelines=pipelines, parent=parent)
    camera.spectral_bins = 15
    camera.pixel_samples = 1

    return camera
