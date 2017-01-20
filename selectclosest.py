import bpy

bl_info = {
	"name": "Select closest",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701201542),
	"blender": (2, 78, 0),
	"location": "View3D > Select > Select closest",
	"description": "Select a vertex closest to any vertex of other selected mesh objects",
	"category": "Experimental development"}


class SelectClosestOp(bpy.types.Operator):
	bl_idname = 'mesh.selectclosestop'
	bl_label = 'Select closest'
	bl_options = {'REGISTER', 'UNDO'}

	# only available in edit mode with some other mesh objects selected
	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' 
			and context.active_object.type == 'MESH'
			and any([o.type == 'MESH'
						for o in set(context.selected_objects) 
								- set([context.active_object])]))

	def execute(self, context):
		# this is about the *slowest* implementation you can imagine
		# (see numpy recipes and bvhtree or kdtree for faster ways
		# to check the closest vertex for many coordinates)
		# but the focus here is on converting between coordinate systems
		bpy.ops.object.editmode_toggle()
		obverts = context.active_object.data.vertices
		obmat = context.active_object.matrix_world
		closest_vertex = None
		distance_squared = 1e30  # big
		for ob in set(context.selected_objects) - set([context.active_object]):
			if ob.type == 'MESH':
				otherverts = ob.data.vertices
				obmatinv = ob.matrix_world.inverted()
				for v1 in obverts:
					# convert to world coords
					v1_world = obmat * v1.co
					# convert to object coords of other object
					v1_object_other = obmatinv * v1_world
					for v2 in otherverts:
						d2 = (v1_object_other - v2.co).length_squared
						if d2 < distance_squared:
							distance_squared = d2
							closest_vertex = v1
		if closest_vertex:
			closest_vertex.select = True
		bpy.ops.object.editmode_toggle()
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		SelectClosestOp.bl_idname,
		text=SelectClosestOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
