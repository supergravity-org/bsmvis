# This script uses bmesh operators to make 2 links of a chain.

import bpy
import bmesh
import math
import mathutils
from mathutils import Vector
import os.path
import sys
from . import support

from .. import ROOT

# Make a new BMesh
bm = bmesh.new()

# ROOT = os.path.dirname(__file__)
print(ROOT)

PI = 3.14159265359

def create_te():
    bpy.ops.group.create(name="te1g")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, size=1)
    obj = bpy.context.object
    obj.name = 'te1'
    dim = obj.dimensions

    mat_high = bpy.data.materials.new("highlight")
    mat_high.diffuse_color = (float(.5), 0.0, 1.0)
    mat_origin = bpy.data.materials.new("highlight_origin")
    mat_origin.diffuse_color = (float(1.0), 0.0, 0.5)
    mat_norm = bpy.data.materials.new("normal")
    mat_norm.diffuse_color = (0.5, 0.5, 0.5)

    obj.active_material = mat_norm

    n = 1
    nsph = 4
    child = None
    all_child = []

    for z in range(0, nsph):
        for y in range(0, nsph):
            for x in range(0, nsph):
                if y%2 == 0:
                    iy = 0.0
                    ix = 0.0
                    iz = 0.0
                else:
                    iy = (dim.y/2.0) * y # + (dim.y * (y-1))
                    ix = 0.0
                    iz = 0.0
                ix = ((dim.x) * x) + ((dim.x/2.0) * y) + ((dim.x/2.0) * z)
                iy = ((dim.y/2.0) * y) + ((math.sqrt(dim.y)/2.0) * y) +  ((math.sqrt(dim.x)/2.0) * z)
                print(dim.z, math.sqrt(dim.z), dim.z/2.0)
                # FIXME: find correct height
                iz = (1.6 * z)

                if x >= nsph - y or \
                   x >= (nsph - y - z):
                    print("skip z:%s y:%s x:%s" % (z, y, x))
                    continue
                # if
                # if x <= y:
                #    continue

                bpy.ops.object.duplicate_move()
                child = bpy.context.object
                child.name = 'te1-%s' % n
                child.location = Vector((ix, iy, iz))
                bpy.ops.object.group_link(group="te1g")
                all_child.append(child)
                n += 1
                # https://de.wikipedia.org/wiki/F%C3%BCnfeck
                # we use the scalefactor a/2 ~ ri math.cos(54°)
                ri = (dim.x/2) / math.cos(0.942477796) #(dim.x)*math.sqrt((5-math.sqrt(5))/2)
                # FIXME: 0.08 is strange :)
                bpy.context.scene.cursor_location = (ix, iy + (ri/2)+0.08, iz + ri)

    child.active_material = mat_origin

    child.select = False
    obj.select = True
    child.name = 'te1'

    bpy.ops.object.delete()
    # change color of first one
    all_child[0].active_material = mat_high
    for child in all_child:
        child.select = True
    bpy.ops.object.join()
    bpy.ops.object.group_link(group="te1g")
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # bpy.ops.object.name = "qp1"

    # bpy.scene.objects.unlink(obj)
    # bpy.data.objects.remove(obj)

def create_qp(common_gap=False):
    pass
    obj = bpy.data.objects['te1']
    obj.select = True

    obj.location = Vector((0.0, 0.0, 0.0))

    numseg = 5
    all_child = []

    for i in range(1, 6):
        bpy.ops.object.duplicate_move_linked()
        child = bpy.context.object
        all_child.append(child)

        child.rotation_mode = 'XYZ'

        # Euler((0.7545587420463562, 0.023988142609596252, 1.02032470703125), 'XYZ')
        # Vector((-1.4611425399780273, 0.9822003841400146, 0.7421605587005615))

        # ix = (obj.dimensions.x/1.3) * i * -1 #0.0 # 2.0 * i
        # iy = (obj.dimensions.x/3.0) * i # 2.0 * i
        ix = 0.0
        # ix = (dim.x/2) / math.cos(0.942477796)
        iy = 0.0
        cfact = 0.0
        if common_gap:
            # 0.128368966
            # 7.35500 deg = 0.128368966 radians
            # negative here as it is reduced rotation around the axis
            cfact = -(0.1283/numseg) * (i)
        angle_z =  (2.0*PI/float(numseg)) * (i) #(i*-1) * ((2 * pi)/5)
        angle_y =  (2.0*PI/float(numseg)) * (i) + cfact #(i*-1) * ((2 * pi)/5)
        angle_x =  (2.0*PI/float(numseg)) * (i)
        child.location = Vector((ix, iy, 0))
        # FIXME: the is strange
        child.rotation_euler = ( 1.013, angle_y, 0)
        # child.select = False
    child.select = False
    obj.select = True
    bpy.ops.object.delete()

    for c in all_child:
        c.select = True
    bpy.ops.object.join()
    child.name = 'qp1'

    # obj.delete()
def create_qb():
    obj = bpy.data.objects['qp1']
    obj.select = True

    obj.location = Vector((0.0, 0.0, 0.0))

    numseg = 12
    all_child = []

    return

    for i in range(1, 2):
        bpy.ops.object.duplicate_move_linked()
        child = bpy.context.object
        all_child.append(child)

        child.rotation_mode = 'XYZ'

        ix = 0.0
        # ix = (dim.x/2) / math.cos(0.942477796)
        iy = 0.0
        cfact = 0.0
        angle_z =  (2.0*PI/float(numseg)) * (i) #(i*-1) * ((2 * pi)/5)
        angle_y =  (2.0*PI/float(numseg)) * (i) + cfact #(i*-1) * ((2 * pi)/5)
        angle_x =  (2.0*PI/float(numseg)) * (i)
        child.location = Vector((ix, iy, 0))
        # FIXME: the is strange
        child.rotation_euler = ( angle_x, 0.0, 0)
        #bpy.context.scene.cursor_location = (ix, iy + (ri/2)+0.08, iz + ri)
        # child.select = False




def create_prism():
    support.clear_scene()
    create_te()
    create_qp(True)
    create_qb()




"""
# Add a circle XXX, should return all geometry created, not just verts.
bmesh.ops.create_circle(
        bm,
        cap_ends=False,
        diameter=0.2,
        segments=8)


# Spin and deal with geometry on side 'a'
edges_start_a = bm.edges[:]
geom_start_a = bm.verts[:] + edges_start_a
ret = bmesh.ops.spin(
        bm,
        geom=geom_start_a,
        angle=math.radians(180.0),
        steps=8,
        axis=(1.0, 0.0, 0.0),
        cent=(0.0, 1.0, 0.0))
edges_end_a = [ele for ele in ret["geom_last"]
               if isinstance(ele, bmesh.types.BMEdge)]
del ret


# Extrude and create geometry on side 'b'
ret = bmesh.ops.extrude_edge_only(
        bm,
        edges=edges_start_a)
geom_extrude_mid = ret["geom"]
del ret


# Collect the edges to spin XXX, 'extrude_edge_only' could return this.
verts_extrude_b = [ele for ele in geom_extrude_mid
                   if isinstance(ele, bmesh.types.BMVert)]
edges_extrude_b = [ele for ele in geom_extrude_mid
                   if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary]
bmesh.ops.translate(
        bm,
        verts=verts_extrude_b,
        vec=(0.0, 0.0, 1.0))


# Create the circle on side 'b'
ret = bmesh.ops.spin(
        bm,
        geom=verts_extrude_b + edges_extrude_b,
        angle=-math.radians(180.0),
        steps=8,
        axis=(1.0, 0.0, 0.0),
        cent=(0.0, 1.0, 1.0))
edges_end_b = [ele for ele in ret["geom_last"]
               if isinstance(ele, bmesh.types.BMEdge)]
del ret


# Bridge the resulting edge loops of both spins 'a & b'
bmesh.ops.bridge_loops(
        bm,
        edges=edges_end_a + edges_end_b)


# Now we have made a links of the chain, make a copy and rotate it
# (so this looks something like a chain)

ret = bmesh.ops.duplicate(
        bm,
        geom=bm.verts[:] + bm.edges[:] + bm.faces[:])
geom_dupe = ret["geom"]
verts_dupe = [ele for ele in geom_dupe if isinstance(ele, bmesh.types.BMVert)]
del ret

# position the new link
bmesh.ops.translate(
        bm,
        verts=verts_dupe,
        vec=(0.0, 0.0, 2.0))
bmesh.ops.rotate(
        bm,
        verts=verts_dupe,
        cent=(0.0, 1.0, 0.0),
        matrix=mathutils.Matrix.Rotation(math.radians(90.0), 3, 'Z'))

# Done with creating the mesh, simply link it into the scene so we can see it

# Finish up, write the bmesh into a new mesh
me = bpy.data.meshes.new("Mesh")
bm.to_mesh(me)
bm.free()


# Add the mesh to the scene
scene = bpy.context.scene
obj = bpy.data.objects.new("Object", fpl)
scene.objects.link(obj)

# Select and make active
scene.objects.active = obj
obj.select = True
"""
