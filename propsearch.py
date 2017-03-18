#  propsearch.py
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

bl_info = {
	"name": "Propsearch example",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701141546),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Propsearch example",
	"description": "Put and object next to another one",
	"category": "Experimental development"}


class PropsearchOp(bpy.types.Operator):
	bl_idname = 'mesh.propsearch'
	bl_label = 'Propsearch example'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	other = StringProperty(name="Other object")

	def draw(self, context):
		layout = self.layout
		layout.prop_search(self,'other',bpy.data,'objects')

	def execute(self, context):
		if self.other in bpy.data.objects:
			other = bpy.data.objects[self.other]
			ob = context.active_object
			ob.location = other.location
			ob.location.x += 1
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		PropsearchOp.bl_idname,
		text=PropsearchOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
