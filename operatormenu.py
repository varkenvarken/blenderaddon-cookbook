import bpy

bl_info = {
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701151551),
	"blender": (2, 78, 0),
	"location": "View3D > Select > Similar > Dummy Op",
	"description": "A dummy operator",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyopmenu'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		return {"FINISHED"}

class VIEW3D_MT_edit_mesh_extra(bpy.types.Menu):
    bl_label = "Extra"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.dummyopmenu", text="Dummy 1")
        layout.operator("mesh.dummyopmenu", text="Dummy 2")

def menu_func(self, context):
	self.layout.separator()
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='PLUGIN')
	self.layout.separator()
	self.layout.menu('VIEW3D_MT_edit_mesh_extra')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh_select_similar.remove(menu_func)
	bpy.utils.unregister_module(__name__)
