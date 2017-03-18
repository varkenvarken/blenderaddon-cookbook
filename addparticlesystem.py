#  addparticlesystem.py
#
#  (c) 2017 Michel Anders
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.


import bpy
from bpy.props import StringProperty
from random import randint

bl_info = {
	"name": "Add particle system",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701141632),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Add particle system",
	"description": "Add a particle system with 100 particles",
	"category": "Experimental development"}


class AddParticlesOp(bpy.types.Operator):
	bl_idname = 'mesh.addparticlesystem'
	bl_label = 'Add particle system'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		settings = 'Particles100'
		if settings not in bpy.data.particles:
			settings = bpy.data.particles.new(settings)
		else:
			settings = bpy.data.particles[settings]
		settings.count = 100

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
		AddParticlesOp.bl_idname,
		text=AddParticlesOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
