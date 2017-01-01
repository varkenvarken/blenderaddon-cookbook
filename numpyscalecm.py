import bpy, bmesh
from bpy.props import FloatProperty
from mathutils import Vector
import numpy as np
from time import time

bl_info = {
	"name": "Numpy Scale",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701011501),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Numpy Scale",
	"description": "Scale around center of mass",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class RegularScaleOp(bpy.types.Operator):
	bl_idname = 'mesh.regularscaleop'
	bl_label = 'Regular Scale CM'
	bl_options = {'REGISTER', 'UNDO'}

	scale = FloatProperty(name='Scale', default=1)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# mesh must be in object mode
		ob = context.active_object
		start = time()
		me = ob.data
		count = len(me.vertices)
		# calculate center of mass
		cm = sum((v.co for v in me.vertices), Vector())
		if count > 1:
			cm /= count
		# scale the vertex coordinates
		for v in me.vertices:
			v.co = cm + (v.co - cm) * self.scale
		print("{count} verts scaled in {t:.2f} seconds".format(
					t=time()-start, count=count))
		return {"FINISHED"}

class NumpyScaleOp(bpy.types.Operator):
	bl_idname = 'mesh.numpyscaleop'
	bl_label = 'Numpy Scale CM'
	bl_options = {'REGISTER', 'UNDO'}

	scale = FloatProperty(name='Scale', default=1)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT' and
				context.active_object.type == 'MESH')

	def execute(self, context):
		# mesh must be in object mode
		ob = context.active_object
		start = time()
		me = ob.data
		# get vertex coordinates
		count = len(me.vertices)
		shape = (count, 3)
		verts = np.empty(count*3, dtype=np.float32)
		me.vertices.foreach_get('co', verts)
		verts.shape = shape
		# calculate center of mass
		cm = np.average(verts,axis=0)
		# scale the vertex coordinates
		verts = cm + (verts - cm ) * np.float32(self.scale)
		# return coordinates, flatten the array first
		verts.shape = count*3
		me.vertices.foreach_set('co', verts)
		print("{count} verts scaled in {t:.2f} seconds".format(
					t=time()-start, count=count))
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		RegularScaleOp.bl_idname,
		text=RegularScaleOp.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		NumpyScaleOp.bl_idname,
		text=NumpyScaleOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
