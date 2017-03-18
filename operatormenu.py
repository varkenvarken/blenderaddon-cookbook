#  operatormenu.py
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
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701151551),
	"blender": (2, 78, 0),
	"location": "View3D > Select > Similar > Dummy Op",
	"description": "A dummy operator",
	"category": "Experimental development"}


class DummyOp(bpy.types.Operator):
	bl_idname = 'mesh.dummyopmenu'
	bl_label = 'Dummy Operator'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		return {"FINISHED"}

class VIEW3D_MT_edit_mesh_extra(bpy.types.Menu):
    bl_label = "Extra"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.dummyopmenu", text="Dummy 1")
        layout.operator("mesh.dummyopmenu", text="Dummy 2")

def menu_func(self, context):
	self.layout.separator()
	self.layout.operator(
		DummyOp.bl_idname,
		text=DummyOp.bl_label,
		icon='PLUGIN')
	self.layout.separator()
	self.layout.menu('VIEW3D_MT_edit_mesh_extra')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_edit_mesh_select_similar.remove(menu_func)
	bpy.utils.unregister_module(__name__)
