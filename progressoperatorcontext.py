import bpy
from time import sleep

bl_info = {
	"name": "Progress Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612251623),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Progress",
	"description": "An operator showing a progress bar",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class ProgressCM:

	def __init__(self, wm=None, steps=100):
		self.running = False
		self.wm = wm
		self.steps = steps
		self.current_step = 0

	def __enter__(self):
		if self.wm:
			self.wm.progress_begin(0, self.steps)
			self.step()
			self.running = True
		return self

	def __exit__(self, *args):
		self.running = False
		if self.wm:
			self.wm.progress_end()
			self.wm = None
		else:
			print("Done.\n")

	def step(self, amount=1):
		self.current_step += amount
		self.current_step = min(self.current_step, self.steps)
		if self.wm:
			self.wm.progress_update(self.current_step)
		else:
			print("Step "
					+ str(self.current_step)
					+ "/" + str(self.steps))

class ProgressOpContext(bpy.types.Operator):
	bl_idname = 'mesh.progressopcontext'
	bl_label = 'Progress'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		with ProgressCM(wm=context.window_manager,
						steps=5) as progress:
			for i in range(5):
				progress.step(1)
				sleep(1)  # imagine we do something heavy here

		return {"FINISHED"}


# we don't need a menu entry but it's
# easier than hitting spacebar and searching


def menu_func(self, context):
	self.layout.operator(
		ProgressOpContext.bl_idname,
		text=ProgressOpContext.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
