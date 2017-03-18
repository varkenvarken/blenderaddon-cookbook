#  selectclosest.py
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

bl_info = {
	"name": "Select closest",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701201542),
	"blender": (2, 78, 0),
	"location": "View3D > Select > Select closest",
	"description": "Select a vertex closest to any vertex of other selected mesh objects",
	"category": "Experimental development"}


class SelectClosestOp(bpy.types.Operator):
	bl_idname = 'mesh.selectclosestop'
	bl_label = 'Select closest'
	bl_options = {'REGISTER', 'UNDO'}

	# only available in edit mode with some other mesh objects selected
	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH' 
			and context.active_object.type == 'MESH'
			and any([o.type == 'MESH'
						for o in set(context.selected_objects) 
								- set([context.active_object])]))

	def execute(self, context):
		# this is about the *slowest* implementation you can imagine
		# (see numpy recipes and bvhtree or kdtree for faster ways
		# to check the closest vertex for many coordinates)
		# but the focus here is on converting between coordinate systems
		bpy.ops.object.editmode_toggle()
		obverts = context.active_object.data.vertices
		obmat = context.active_object.matrix_world
		closest_vertex = None
		distance_squared = 1e30  # big
		for ob in set(context.selected_objects) - set([context.active_object]):
			if ob.type == 'MESH':
				otherverts = ob.data.vertices
				obmatinv = ob.matrix_world.inverted()
				for v1 in obverts:
					# convert to world coords
					v1_world = obmat * v1.co
					# convert to object coords of other object
					v1_object_other = obmatinv * v1_world
					for v2 in otherverts:
						d2 = (v1_object_other - v2.co).length_squared
						if d2 < distance_squared:
							distance_squared = d2
							closest_vertex = v1
		if closest_vertex:
			closest_vertex.select = True
		bpy.ops.object.editmode_toggle()
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		SelectClosestOp.bl_idname,
		text=SelectClosestOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
