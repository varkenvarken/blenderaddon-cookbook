#  vertexdatalayer.py
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

bl_info = {
	"name": "Vertex Custom Data",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701011034),
	"blender": (2, 78, 0),
	"location": "View3D > Edit > Vertex Custom Data",
	"description": "Change/Add Vertex Custom Data",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class VertexCustomData(bpy.types.Operator):
	bl_idname = 'mesh.vertexcustomdata'
	bl_label = 'Vertex Custom Data'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		ob = context.active_object
		# mesh must be in edit mode!
		bm = bmesh.from_edit_mesh(ob.data)
		bl = bm.verts.layers.bevel_weight.new('Vertex bevel')
		for v in bm.verts:
			if v.co.x > 0:
				v[bl] = 1.0

		bmesh.update_edit_mesh(ob.data)
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		VertexCustomData.bl_idname,
		text=VertexCustomData.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.utils.unregister_module(__name__)
