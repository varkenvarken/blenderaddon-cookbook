#  edgeproperties.py
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


import bpy, bmesh
from random import random

bl_info = {
	"name": "Edge Properties",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701010921),
	"blender": (2, 78, 0),
	"location": "View3D > Mesh > Edge Properties",
	"description": "Edge Properties",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class EdgePropertiesOp(bpy.types.Operator):
	bl_idname = 'mesh.edgepropertiesop'
	bl_label = 'Edge Properties'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		bpy.ops.mesh.select_all(action='DESELECT')
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		# select all edges that stradle a (local) axis
		for e in bm.edges:
			a = e.verts[0].co
			b = e.verts[1].co
			# mutliplying two vectors a * b gives dot, not
			# componentwise multiplication so we do this
			# ourself. If any component (x,y or z) is
			# positive for one vertex but negative for
			# the other the product will be negative
			if any(c1*c2 < 0 for c1,c2 in zip(a,b)) :
				e.select = True
		# make sure we also select verts and faces
		bm.select_flush(True)

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		EdgePropertiesOp.bl_idname,
		text=EdgePropertiesOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
