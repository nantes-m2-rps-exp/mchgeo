from ._constants import LIST_OF_DEIDS
from ._constants import DATA_DIR
import os.path
import json
import math


def _read_geometry(geomFile):
    try:
        with open(geomFile) as f:
            g = json.load(f)
            return g
    except IOError:
        print("could not read file", geomFile)


def _asJSON():
    geomFile = os.path.join(DATA_DIR, "de-geometry.json")
    try:
        return _read_geometry(geomFile)
    except IOError:
        return {}


def feature(deid: int):
    assert(deid in LIST_OF_DEIDS), "{} is not a valid detection element ID".format(deid)
    feat = [f for f in JSON if f["properties"]["deid"] == deid]
    return feat[0]


def polygon(deid: int):
    feat = feature(deid)
    return feat["geometry"]


def transformation(deid: int):
    feat = feature(deid)
    props = feat["properties"]
    trans = {k: v for k, v in props.items() if k in ["tx", "ty", "tz",
                                                     "yaw", "pitch", "roll"]}
    return trans


def offset(deid: int):
    feat = feature(deid)
    props = feat["properties"]
    return {k: v for k, v in props.items() if k in ["x", "y"]}


def angles2matrix(yaw, pitch, roll, degrees=True):
    if degrees == True:
        yaw = math.radians(yaw)
        pitch = math.radians(pitch)
        roll = math.radians(roll)

    sinpsi = math.sin(roll)
    cospsi = math.cos(roll)
    sinthe = math.sin(pitch)
    costhe = math.cos(pitch)
    sinphi = math.sin(yaw)
    cosphi = math.cos(yaw)
    return [
        costhe * cosphi,
        -costhe * sinphi,
        sinthe,
        sinpsi * sinthe * cosphi + cospsi * sinphi,
        -sinpsi * sinthe * sinphi + cospsi * cosphi,
        -costhe * sinpsi,
        -cospsi * sinthe * cosphi + sinpsi * sinphi,
        cospsi * sinthe * sinphi + sinpsi * cosphi,
        costhe * cospsi
    ]

JSON = _asJSON()
