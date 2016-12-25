import bpy

bl_info = {
	"name": "Dummy Operation",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612251157),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Add Mesh"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyop'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

# no draw function, add one if needed

# the execute function is empty
	def execute(self, context):
		return {"FINISHED"}


# we don't need a menu entry but it's
# easier than hitting spacebar and searching


def menu_func(self, context):
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
