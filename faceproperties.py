import bpy, bmesh
from random import random

bl_info = {
	"name": "Face Properties",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701010921),
	"blender": (2, 78, 0),
	"location": "View3D > Mesh > Face Properties",
	"description": "Face Properties",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class FacePropertiesOp(bpy.types.Operator):
	bl_idname = 'mesh.facepropertiesop'
	bl_label = 'Face Properties'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		bpy.ops.mesh.select_all(action='DESELECT')
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		# get all edges that stradle a (local) axis
		# we do not select anything here
		for e in bm.edges:
			a = e.verts[0].co
			b = e.verts[1].co
			# mutliplying two vectors a * b gives dot, not
			# componentwise multiplication so we do this
			# ourself. If any component (x,y or z) is
			# positive for one vertex but negative for
			# the other the product will be negative
			if any(c1*c2 < 0 for c1,c2 in zip(a,b)) :
				e.smooth = True
				for f in e.link_faces:
					f.smooth = True

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		FacePropertiesOp.bl_idname,
		text=FacePropertiesOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
