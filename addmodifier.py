import bpy

bl_info = {
	"name": "Add Modifier",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612291622),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Object > Add Modifier",
	"description": "Add a modifier",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class AddModifier(bpy.types.Operator):
	bl_idname = 'mesh.addmodifier'
	bl_label = 'Add Modifier'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

#https://www.blender.org/api/blender_python_api_current/bpy.types.ObjectModifiers.html

	def execute(self, context):
		ob = context.active_object
		mod = ob.modifiers.new('NewModifier','SUBSURF')
		# all objects have a modifiers attribute, but not
		# all type of object can take modifiers, for example
		# a lamp cannot. In that case new() will return None
		if mod:
			# some properties are common to all types
			mod.show_in_editmode = True
			# others are type specific
			mod.render_levels = 2
			mod.levels = 2
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		AddModifier.bl_idname,
		text=AddModifier.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
