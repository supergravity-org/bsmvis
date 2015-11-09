# This script uses bmesh operators to make 2 links of a chain.

import bpy
import bmesh
import math
import mathutils
import os.path
import sys
import types
import importlib

ROOT = '/home/poelzi/Projects/bsm-sg/bsmvis/src'

if ROOT not in sys.path:
    sys.path.append(ROOT)

print(sys.path)

import bsmvis.blender.support
bsmvis.blender.support.reload()

import bsmvis.blender.prism
from bsmvis.blender.prism import create_prism

create_prism()
