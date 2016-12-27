import bpy

bl_info = {
	"name": "Modal Operator Pass Thru",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612270806),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Modal Operator",
	"description": "Example of a modal operator that passes some events",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class ModalOpPT(bpy.types.Operator):
	bl_idname = 'mesh.modalop_pt'
	bl_label = 'Modal Operator Pass Thru'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def modal(self, context, event):
		context.area.header_text_set(
			"event: {e.type} {e.value} ({e.mouse_x},{e.mouse_y})".format(e=event))
		context.area.tag_redraw()

		if event.type in {'RIGHTMOUSE', 'ESC'}:
			context.area.header_text_set()
			context.area.tag_redraw()
			return {'CANCELLED'}

		# allows changing to/from edit mode
		if event.type in {'TAB'}:
			context.area.header_text_set()
			context.area.tag_redraw()
			return {'PASS_THROUGH'}

		# allows view rotation
		if ( 	event.type in {'MIDDLEMOUSE'} 
			or (event.type in {'MOUSEMOVE'} and event.value == 'PRESS')):
			return {'PASS_THROUGH'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		# this is what makes an operator modal:
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		ModalOpPT.bl_idname,
		text=ModalOpPT.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
