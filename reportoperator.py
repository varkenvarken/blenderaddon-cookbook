import bpy
from bpy.props import EnumProperty, StringProperty
from time import sleep

bl_info = {
	"name": "Report Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612251157),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Report",
	"description": "An operator showing various reports",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class ReportOp(bpy.types.Operator):
	bl_idname = 'mesh.reportop'
	bl_label = 'Report'
	bl_options = {'REGISTER', 'UNDO'}

	report_type = EnumProperty(
		name='Type',
		description='Type of report',
		items=[
			('DEBUG', 'DEBUG', 'DEBUG', 1),
			('INFO', 'INFO', 'INFO', 2),
			('OPERATOR', 'OPERATOR', 'OPERATOR', 3),
			('PROPERTY', 'PROPERTY', 'PROPERTY', 4),
			('WARNING', 'WARNING', 'WARNING', 5),
			('ERROR', 'ERROR', 'ERROR', 6),
			('ERROR_INVALID_INPUT', 'ERROR_INVALID_INPUT', 'ERROR_INVALID_INPUT', 7),
			('ERROR_INVALID_CONTEXT', 'ERROR_INVALID_CONTEXT', 'ERROR_INVALID_CONTEXT', 8),
			('ERROR_OUT_OF_MEMORY', 'ERROR_OUT_OF_MEMORY', 'ERROR_OUT_OF_MEMORY', 9)
		])

	message = StringProperty(name='Message')

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		self.report({self.report_type}, self.message)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ReportOp.bl_idname,
		text=ReportOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
