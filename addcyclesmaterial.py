import bpy

bl_info = {
	"name": "Add Cycles Material",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701061038),
	"blender": (2, 78, 0),
	"location": "Node > Add > Add Cycles Materail",
	"description": "A a basic cycles material",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class AddCyclesMat(bpy.types.Operator):
	bl_idname = 'mode.add_cycles_material'
	bl_label = 'Add Cycles Material'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return ((context.active_object is not None )
			and (context.scene.render.engine == 'CYCLES'))

	def execute(self, context):
		bpy.ops.object.material_slot_add()
		ob = context.active_object
		slot = ob.material_slots[ob.active_material_index]
		mat = bpy.data.materials.new('Cycles material')
		mat.use_nodes = True
		slot.material = mat
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		AddCyclesMat.bl_idname,
		text=AddCyclesMat.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.NODE_MT_add.append(menu_func)


def unregister():
	bpy.types.NODE_MT_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
