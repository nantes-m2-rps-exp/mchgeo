# CERN Alice MCH Geometry Python Package

## Usage

See [sample notebook](shapely.ipynb).

## How to (re)generate data (for developpers only)

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

## Generate geometry file

```shell
python generate.py
```

This command requires the MCH mapping API to be running in `localhost:8888` and
will output a `mchgeo/data/de-geometry.json` file which contains a list of 2D
polygons (one per detection element) describing the envelops of the detection
elements and the associated 3D geometry transformations needed to "position"
them in space.

