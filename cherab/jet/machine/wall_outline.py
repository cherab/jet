
# Copyright 2014-2017 United Kingdom Atomic Energy Authority
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

import os
import json
import numpy as np
import matplotlib.pyplot as plt

from cherab.core.math.mask import PolygonMask2D


def firstwall(pulse=92782):
    """
    Returns the coordinates of the JET first wall for the specified pulse.

    :param pulse: JET pulse number.
    :return: A Nx2 numpy array of coordinates or None if no data available.
    """

    path = os.path.join(os.path.dirname(__file__), "first_wall.json")

    with open(path) as f:
        walls = json.load(f)

    # crude, but we have a very limited number of first walls
    for wall in walls:
        if wall["end"]:
            if wall["start"] <= pulse <= wall["end"]:
                return np.array(wall["polygon"])
        else:
            if pulse >= wall["start"]:
                return np.array(wall["polygon"])
    return None


def plot_jet_wall_outline(pulse=92782, style='k'):

    outline = firstwall(pulse=pulse)
    for i in range(outline.shape[0] - 1):
        plt.plot([outline[i, 0], outline[i+1, 0]],
                 [outline[i, 1], outline[i+1, 1]], style)
    plt.axis('equal')


def get_jet_wall_mask(pulse=92782):

    return PolygonMask2D(firstwall(pulse=pulse))


if __name__ == '__main__':
    plot_jet_wall_outline()
    plt.show()
