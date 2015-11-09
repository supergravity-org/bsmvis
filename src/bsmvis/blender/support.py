# The following function is adapted from
# Nick Keeline "Cloud Generator" addNewObject
# from object_cloud_gen.py (an addon that comes with the Blender 2.6 package)
#
import bpy
import os
from .. import ROOT
import importlib
import sys


def reload():
    importlib
    for name, mod in sys.modules.items():
        if not hasattr(mod, '__file__'):
            continue
        if mod.__file__.startswith(ROOT):
            print("reload:", name)
            try:
                importlib.reload(mod)
            except Exception as e:
                print("error reloading:")
                import traceback
                traceback.print_exc()


def clear_scene(scene=None):
    if not scene:
        scene = bpy.context.scene
    for obj in scene.objects:
        scene.objects.unlink(obj)
        bpy.data.objects.remove(obj)


def load_fp(src, name):
    if bpy.data.objects.find(name):
        filepath = os.path.join(ROOT, src)
        # link all objects starting with 'A'
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            print(data_from.objects)
            data_to.objects = [n for n in data_from.objects if n == name]
            #data_to.objects['fpl_real'] = data_from.objects['fpl_real']

        #bpy.ops.import_mesh.ply(filepath=os.path.join(ROOT, "fp/fpl_real.blend"))

    rv = bpy.data.objects[name]
    rv
    return rv


def duplicateObject(scene, name, copyobj):

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)

    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location

    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True

    return ob_new

def get_fpl():
    return load_fp(os.path.join(ROOT, "fp/fpl_real.blend"), 'FP1_real')
