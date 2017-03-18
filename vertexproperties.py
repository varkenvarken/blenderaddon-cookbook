#  vertexproperties.py
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
	"name": "Vertex Properties",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701010921),
	"blender": (2, 78, 0),
	"location": "View3D > Mesh > Vertex Properties",
	"description": "Vertex Properties",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class VertexPropertiesOp(bpy.types.Operator):
	bl_idname = 'mesh.vertexpropertiesop'
	bl_label = 'Vertex Properties'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		bpy.ops.mesh.select_all(action='DESELECT')
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		# select all vertices on the (local) positive x-axis
		for v in bm.verts:
			if v.co.x >= -0.0001: # accuracy!
				v.select = True
		# make sure we also select edges and faces if all
		# the constituent verts are selected
		bm.select_flush(True)
		# to index individual elements we must ensure they
		# indexable
		bm.verts.ensure_lookup_table()
		# this is not the most elegant way to randomly scale
		# every second vertex but it illustrates how you can
		# access a single vertex with an index
		for i in range(len(bm.verts)):
			if i%2 :
				bm.verts[i].co *= 0.95 + random() * 0.1

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		VertexPropertiesOp.bl_idname,
		text=VertexPropertiesOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
