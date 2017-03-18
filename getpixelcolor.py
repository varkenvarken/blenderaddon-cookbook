#  getpixelcolor.py
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
import bgl

bl_info = {
	"name": "Get Pixel",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701081540),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Get Pixel",
	"description": "Get pixel color from 3d viewport",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class GetPixel(bpy.types.Operator):
	bl_idname = 'scene.getpixel'
	bl_label = 'Get pixel color'
	bl_options = {'REGISTER', 'UNDO'}

	def modal(self, context, event):
		if ((event.type in {'RIGHTMOUSE', 'ESC'})
			or
			(event.type == 'LEFTMOUSE' and event.value == 'RELEASE')):
			context.area.header_text_set()
			context.window.cursor_modal_restore()
			context.area.tag_redraw()
			return {'CANCELLED'}
		elif (event.type in {'LEFTMOUSE', 'MOUSEMOVE'}
					and event.value == 'PRESS'):
				bgl.glReadPixels(event.mouse_x, event.mouse_y,
						1,1 , bgl.GL_RGB, bgl.GL_FLOAT, self.buf)
				t = "{c[0]:.3f},{c[1]:.3f},{c[2]:.3f}".format(c=self.buf[0])
				context.area.header_text_set(t)
				context.area.tag_redraw()
				return {'RUNNING_MODAL'}
		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		self.buf = bgl.Buffer(bgl.GL_FLOAT, [1, 3])
		context.window.cursor_modal_set('EYEDROPPER')
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		GetPixel.bl_idname,
		text=GetPixel.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
