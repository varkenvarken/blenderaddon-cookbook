#  addobject.py
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
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras.object_utils import object_data_add

bl_info = {
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201703041434),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Dummy Op",
	"description": "A dummy operator",
	"category": "Experimental development"}


class DummyOpObject(bpy.types.Operator, AddObjectHelper):
	bl_idname = 'mesh.dummyopobject'
	bl_label = 'Add Object'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		sqrt2 = 1.4142135623730951
		verts = [[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0],[0,0,-sqrt2],[0,0,sqrt2]]
		faces = [[0,4,1],[1,4,2],[2,4,3],[3,4,0],[0,1,5],[1,2,5],[2,3,5],[3,0,5]]
		mesh = bpy.data.meshes.new(name="New Object Mesh")
		mesh.from_pydata(verts, [], faces)
		object_data_add(context, mesh, operator=self)
		return {"FINISHED"}

def menu_func(self, context):
	self.layout.operator(
		DummyOpObject.bl_idname,
		text=DummyOpObject.bl_label,
		icon='PLUGIN')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
