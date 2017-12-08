
import os
import re

from raysect.core.math import Point3D, Vector3D
from cherab.tools.observers.spectroscopic import LineOfSightGroup, SpectroscopicSightLine


SURF_DATABASE = '/home/flush/surf/input/overlays_db.dat'
KB5_SURF_HEADER = "^\*Bolometry/KB5/[A-Za-z0-9]*/kb5/([0-9]*)/([0-9]*)"
KB5_RECORD_ROW = "^'([A-Z0-9]*)\s*([0-9]*)\s*\(([A-Za-z0-9]*)\)'\s*" \
                 "(-?[0-9]*.[0-9]*)\s*(-?[0-9]*.[0-9]*)\s*(-?[0-9]*.[0-9]*)\s*(-?[0-9]*.[0-9]*)"


def load_kb5_sightlines(shot_number, parent=None):

    if not os.path.isfile(SURF_DATABASE):
        raise IOError('SURF database file could not be found.')

    surf_fh = open(SURF_DATABASE, 'r')
    surf_db = surf_fh.readlines()

    for i, line in enumerate(surf_db):

        if line[0] == '*':
            match = re.match(KB5_SURF_HEADER, line)
            if match:
                start_shot = int(match.group(1))
                end_shot = int(match.group(2))
                if start_shot <= shot_number <= end_shot:
                    break
    else:
        raise ValueError("KB5 settings for the requested shot number are not available in the SURF database.")

    kb5_record = []
    while line[0] != "*" or line[0] != "£":
        kb5_record.append(line)
        i += 1
        line = surf_db[i]

    kb5v = LineOfSightGroup(name="KB5V", parent=parent)
    kb5h = LineOfSightGroup(name="KB5H", parent=parent)

    for row in kb5_record:
        match = re.match(KB5_RECORD_ROW, row)
        if match:

            detector = match.group(1)
            channel_id = match.group(2)
            long_id = match.group(3)
            r_start = float(match.group(4))
            z_start = float(match.group(5))
            r_end = float(match.group(6))
            z_end = float(match.group(7))

            point = Point3D(r_start, 0, z_start)
            direction = Vector3D(r_end-r_start, 0, z_end-z_start).normalise()

            sightline = SpectroscopicSightLine(point, direction, name=detector+channel_id)

            if detector == "KB5V":
                kb5v.add_sight_line(sightline)
            elif detector == "KB5H":
                kb5h.add_sight_line(sightline)
            else:
                raise ValueError("detector name should be 'KB5V' or 'KB5H'")

    return kb5v, kb5h
