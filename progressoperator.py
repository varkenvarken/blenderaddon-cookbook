import bpy
from time import sleep

bl_info = {
	"name": "Progress Operation",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612251157),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Progress",
	"description": "An operator showing a progress bar",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Add Mesh"}


class ProgressOp(bpy.types.Operator):
	bl_idname = 'mesh.progressop'
	bl_label = 'Progress'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

# no draw function, add one if needed

# the execute function is empty
	def execute(self, context):
		wm = context.window_manager
		wm.progress_begin(0, 5)
		for i in range(5):
			wm.progress_update(i)
			sleep(1)  # imagine we do something heavy here
		wm.progress_end()
		return {"FINISHED"}


# we don't need a menu entry but it's
# easier than hitting spacebar and searching


def menu_func(self, context):
	self.layout.operator(
		ProgressOp.bl_idname,
		text=ProgressOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
