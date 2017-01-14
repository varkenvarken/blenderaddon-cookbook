import bpy
from bpy.props import StringProperty, IntProperty
from random import randint

bl_info = {
	"name": "Add particle system",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701141649),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Add particle system",
	"description": "Add a particle system with default # of particles set in add-on prefs",
	"category": "Experimental development"}

class ParticlePrefs(bpy.types.AddonPreferences):
	bl_idname = __name__  # give settings the name of the python module

	particle_count = IntProperty(
		name="Default # of particles",
		default=100, min=1, soft_max=1000)

	# unlike a Operator the draw() function of an
	# AddonPreferences derived class must be overridden to
	# produce something meaningful. Defined properties are
	# *not* drawn automatically!
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "particle_count")

class AddParticlesOp2(bpy.types.Operator):
	bl_idname = 'mesh.addparticlesystem2'
	bl_label = 'Add particle system'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		prefs = context.user_preferences.addons[__name__].preferences

		settings = 'Particles' + str(prefs.particle_count)

		if settings not in bpy.data.particles:
			settings = bpy.data.particles.new(settings)
		else:
			settings = bpy.data.particles[settings]
		settings.count = prefs.particle_count

		ob = context.active_object
		if ob:
			# a particle system is a modifier! However, we
			# cannot alter properties of this modifier
			pm = ob.modifiers.new('Particles','PARTICLE_SYSTEM')
			if pm:  # could be None if object is Camera or something
				# some things are controlled by the system
				# for instanc the random seed
				pm.particle_system.seed = randint(0,1000000)
				# other by the settings, which is a seperate
				# object that can be shared by different
				# particle systems
				pm.particle_system.settings = settings
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		AddParticlesOp2.bl_idname,
		text=AddParticlesOp2.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
