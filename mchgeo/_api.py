from ._constants import LIST_OF_DEIDS
import json
import math
from importlib.resources import open_text

def _asJSON():
    geomFile= open_text('.'.join((__package__,'data')),'de-geometry.json')
    g = json.load(geomFile)
    return g


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
