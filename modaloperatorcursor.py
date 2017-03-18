#  modaloperatorcursor.py
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
	"name": "Modal Operator Cursor",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201612271052),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Modal Operator",
	"description": "Modal operator with a changed cursor",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class ModalOpCursor(bpy.types.Operator):
	bl_idname = 'mesh.modalopcursor'
	bl_label = 'Modal Operator Cursor'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def modal(self, context, event):
		context.area.tag_redraw()

		if event.type in {'RIGHTMOUSE', 'ESC'}:
			context.window.cursor_modal_restore()
			context.area.tag_redraw()
			return {'CANCELLED'}

		if event.type == 'W' and event.value == 'RELEASE':
			self.cursors.insert(0,self.cursors.pop())
			context.window.cursor_modal_set(self.cursors[0])

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		context.window.cursor_modal_set('CROSSHAIR')
		self.cursors = ['CROSSHAIR', 'WAIT', 'MOVE_X',
			'MOVE_Y', 'KNIFE', 'TEXT', 'PAINT_BRUSH',
			'HAND', 'SCROLL_X', 'SCROLL_Y',
			'SCROLL_XY', 'EYEDROPPER']
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		ModalOpCursor.bl_idname,
		text=ModalOpCursor.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
