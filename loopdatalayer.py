import bpy, bmesh

bl_info = {
	"name": "Loop Custom Data",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701011345),
	"blender": (2, 78, 0),
	"location": "View3D > Edit > Loop Custom Data",
	"description": "Change/Add Loop Custom Data",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class LoopCustomData(bpy.types.Operator):
	bl_idname = 'mesh.loopcustomdata'
	bl_label = 'Loop Custom Data'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		# first we replace the active vertex color layer
		cl = bm.loops.layers.color.active
		if cl is None:
			cl = bm.loops.layers.color.new('Col')
		# we set the color to the scaled local coordinates
		# we need to access the loops via face even though
		# bm.loops exists
		bb = ob.bound_box  # docs are wrong this is [8][3], not [24]
		cc = 0,1,2
		pp = 0,1,2,3,4,5,6,7
		ext = [(min(bb[p][c] for p in pp),
				max(bb[p][c] for p in pp))
				for c in cc]
		ext = [(mine, maxe-mine) for mine,maxe in ext]
		ext = [(mine, maxe if abs(maxe) > 1e-7 else 1.0) for mine,maxe in ext]
		for face in bm.faces:
			for loop in face.loops:
				loop[cl] = tuple((c-e[0])/e[1]
						for c,e in zip(loop.vert.co,ext))

		# and we create a uv projection on the xy plane
		uv = bm.loops.layers.uv.active
		if uv is None:
			uv = bm.loops.layers.uv.new('UVmap')
		for face in bm.faces:
			for loop in face.loops:
				loop[uv].uv = loop.vert.co.xy

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		LoopCustomData.bl_idname,
		text=LoopCustomData.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
