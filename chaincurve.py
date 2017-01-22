import bpy
from mathutils import kdtree, Vector

bl_info = {
	"name": "Create a curve between selected objects",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701221448),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Curve between objects",
	"description": """Create a curve between selected objects""",
	"category": "Experimental development"}

def object_list(objects, active=0):
	"""
	Return an approximate shortest path through objects starting at the
	active index using the nearest neighbor heuristic.
	"""

	# calculate a kd tree to quickly answer nearest neighbor queries
	kd = kdtree.KDTree(len(objects))
	for i, ob in enumerate(objects):
		kd.insert(ob.location, i)
	kd.balance()

	current = objects[active]
	chain = [current]  # we start at the chosen object
	added = {active}
	for i in range(1,len(objects)):  # we know how many objects to add
		# when looking for the nearest neighbor we start with two neigbors
		# (because we include the object itself in the search) and if
		# the other neigbors is not yet in the chain we add it, otherwise
		# we expand our search to a maximum of the total number of objects
		for n in range(2,len(objects)):
			neighbors = { index for _,index,_ in kd.find_n(current.location, n) }
			neighbors -= added
			if neighbors:  # strictly speaking we shoudl assert that len(neighbors) == 1
				chain.extend(objects[i] for i in neighbors)
				added |= neighbors
				break
		current = chain[-1]

	return chain

class CurveBetweenObjects(bpy.types.Operator):
	bl_idname = 'curve.curvebetweenobjects'
	bl_label = 'Curve between objects'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT'
			and len(context.selected_objects) > 1)

	def execute(self, context):
		so = context.selected_objects.copy()
		objects = object_list(so, so.index(context.active_object))

		for ob in objects:
			ob.select = False

		midpoint = sum((ob.location for ob in objects),Vector()) / len(objects) # poll() guarantees we don't get a divide by zero

		curve = bpy.data.curves.new(name='Curve', type='CURVE')
		curve.dimensions = '3D'
		curve.bevel_depth = 0.01
		spline = curve.splines.new(type='BEZIER')
		spline.bezier_points.add(len(objects)-1)  # default curve has 1 point
		for ob,bp in zip(objects,spline.bezier_points):
			bp.co = ob.location - midpoint  # subtract will generate a new vector
			bp.handle_left_type = 'AUTO'
			bp.handle_right_type = 'AUTO'

		ob = bpy.data.objects.new(name='Curve',object_data=curve)
		ob.location = midpoint
		context.scene.objects.link(ob)

		context.scene.objects.active = ob
		ob.select = True

		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		CurveBetweenObjects.bl_idname,
		text=CurveBetweenObjects.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
