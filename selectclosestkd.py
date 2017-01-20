import bpy
from mathutils import kdtree

bl_info = {
	"name": "Select closest kd",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701201629),
	"blender": (2, 78, 0),
	"location": "View3D > Select > Select closest kd",
	"description": "Select a vertex closest to any vertex of other selected mesh objects using a kd tree",
	"category": "Experimental development"}


class SelectClosestKDOp(bpy.types.Operator):
	bl_idname = 'mesh.selectclosestkdop'
	bl_label = 'Select closest kd'
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
		bpy.ops.object.editmode_toggle()
		obverts = context.active_object.data.vertices
		obmat = context.active_object.matrix_world

		size = len(obverts)
		kd = kdtree.KDTree(size)
		for i, v in enumerate(obverts):
			kd.insert(obmat * v.co, i)  # store in world coords
		kd.balance()

		closest_vertex = -1
		closest_distance = 1e30  # big
		for ob in set(context.selected_objects) - set([context.active_object]):
			if ob.type == 'MESH':
				otherverts = ob.data.vertices
				obmatother = ob.matrix_world
				for v in otherverts:
					# convert to world coords
					v_world = obmatother * v.co
					co, index, dist = kd.find(v_world)
					if dist < closest_distance:
						closest_distance = dist
						closest_vertex = index
		if closest_vertex >= 0:
			obverts[closest_vertex].select = True
		bpy.ops.object.editmode_toggle()
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		SelectClosestKDOp.bl_idname,
		text=SelectClosestKDOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
