#  progressoperator.py
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
from time import sleep

bl_info = {
	"name": "Progress Operation",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612251157),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Progress",
	"description": "An operator showing a progress bar",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}


class ProgressOp(bpy.types.Operator):
	bl_idname = 'mesh.progressop'
	bl_label = 'Progress'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		wm = context.window_manager
		wm.progress_begin(0, 5)
		for i in range(5):
			wm.progress_update(i)
			sleep(1)  # imagine we do something heavy here
		wm.progress_end()
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ProgressOp.bl_idname,
		text=ProgressOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
