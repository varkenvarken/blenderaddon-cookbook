import bpy, bmesh

bl_info = {
	"name": "Edge Custom Data",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701011345),
	"blender": (2, 78, 0),
	"location": "View3D > Edit > Edge Custom Data",
	"description": "Change/Add Edge Custom Data",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class EdgeCustomData(bpy.types.Operator):
	bl_idname = 'mesh.edgecustomdata'
	bl_label = 'Edge Custom Data'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		bl = bm.edges.layers.bevel_weight.active
		# this is a bit better than our vertex example:
		# even though there will be at most one edge bevel
		# weight layer we only create a new one if there
		# isn't an active one.
		# Note that other types of custom data layers may
		# have 0, 1 or more layers!
		if bl is None:
			bl = bm.edges.layers.bevel_weight.new('Edge bevel')
		for e in bm.edges:
			if any(v.co.x > 0 for v in e.verts):
				e[bl] = 1.0

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		EdgeCustomData.bl_idname,
		text=EdgeCustomData.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
