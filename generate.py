import json
from mchgeo import LIST_OF_DEIDS
import os.path
import requests
import sys

DATA_DIR=os.path.abspath(os.path.join(__file__,'..','mchgeo','data'))

def _read_transformations(transformFile):
    try:
        with open(transformFile) as f:
            align=json.load(f)
            alignables=align["alignables"]
            transformations=[t for t in alignables if 'deid' in t.keys()]
            return transformations
    except IOError:
        print("could not read file",transformFile)

def _read_envelops(envelopFile):
    try:
        with open(envelopFile) as f:
            envelops = json.load(f)
            return envelops
    except IOError:
        print("could not read file",envelopFile)


def _run_query(deid:int, bending:bool): 
    request = requests.post('http://localhost:8080/v2/degeo?deid={}&bending={}'.format(deid,bending))
    if request.status_code == 200:
        return request.text
    else:
        raise Exception("Query failed to run by returning code of {}.".format(request.status_code))

def _mapping2json(file=sys.stdout):
    """ print 2D mapping information (from MCH mapping API) for all detection
        elements in JSON format."""
    geo2d=""
    for deid in LIST_OF_DEIDS:
        envelop = _run_query(deid,True)
        geo2d += "{},".format(envelop)

    geo2d = "[{}]".format(geo2d.strip(','))
    print(geo2d,file=file)

def _combine(envelops,transformations):
    shapes=[]
    for de in envelops:
        g=dict()
        g["type"]="Polygon"
        coordinates=[]
        deid=de["id"]
        for v in reversed(de["vertices"]):
            coordinates.append([v["x"],v["y"]])
            g["coordinates"]=[coordinates]
        trans = [t["transform"] for t in transformations if t["deid"]==deid]
        props=dict({
           "deid":deid,
           "bending": de["bending"],
           "x":de["x"],
           "y":de["y"]})
        for k in trans[0].keys():
            props[k]=trans[0][k]
        g2=dict(type="Feature",geometry=g,properties=props)
        shapes.append(g2)
    return shapes

def _combineFiles(file, envelopFile,transformFile):
    """ Combine DE envelop informations (2D, extracted from e.g. MCH mapping REST API)
    and DE (3D) transformations. Both in JSON formats."""
    transformations = _read_transformations(transformFile)
    envelops = _read_envelops(envelopFile)
    shapes = _combine(envelops,transformations)
    print(json.dumps(shapes),file=file)

if __name__ == '__main__':
    envelopFile = os.path.join(DATA_DIR,"de-envelops.json")
    transformFile = os.path.join(DATA_DIR,"de-transformations.json")
    geomFile = os.path.join(DATA_DIR,"de-geometry.json")
    out=open(envelopFile,"w")
    _mapping2json(out)
    out.close()
    outfile=open(geomFile,"w")
    _combineFiles(outfile,envelopFile,transformFile)
    outfile.close()
