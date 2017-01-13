import bpy

bl_info = {
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701131351),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyop'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	radius = bpy.props.FloatProperty(name="Radius",
		default=1.0, min=0.1, max=10.0)

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		# do something simple but visible
		bpy.ops.mesh.primitive_cube_add(radius=self.radius)
		return {"FINISHED"}

def menu_func(self, context):
	# basic operator
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label)
	# with icon
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='MESH_CUBE')
	# other ui elements possible as well
	self.layout.separator()
	# can set values for properties
	# (do for all, because last value is remembered)
	op = self.layout.operator(
		DummyOp.bl_idname,
		text="Big cube",
		icon='ZOOMIN')
	op.radius = 2.0
	op = self.layout.operator(
		DummyOp.bl_idname,
		text="Little cube",
		icon='ZOOMOUT')
	op.radius = 1.0



def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
