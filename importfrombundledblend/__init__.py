import bpy
import os

bl_info = {
	"name": "Import object from bundled .blend",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701131522),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Import Operator",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.importop'
	bl_label = 'Import Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		blend = os.path.join(os.path.dirname(__file__), "objects.blend")
		# load a library and copy a specific object with its
		# dependencies into the current scene
		# loading a library multiple times is harmless
		with bpy.data.libraries.load(blend, link=False) as (data_from, data_to):
			data_to.objects = ['3Rings']
		# at this point bpy.data.objects is update but no
		# object links are added to the scene yet
		# note that inside the context manager data_to.objects
		# was a list of names but now we left the context it
		# is transnuted into a list of objects!
		for ob in data_to.objects:
			context.scene.objects.link(ob)
		context.scene.update()
		return {"FINISHED"}

def menu_func(self, context):
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label)


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
