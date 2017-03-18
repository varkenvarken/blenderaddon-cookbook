#  coords3dto2d.py
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
import blf
from bpy_extras import view3d_utils

bl_info = {
	"name": "3D Coords to 2D",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701081438),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Show coords",
	"description": "Show coords of vertices",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

running = False
handler = None

def coords_handler(context):
	ob = context.active_object
	if ob:
		loc2d = view3d_utils.location_3d_to_region_2d(
			context.region,
			context.space_data.region_3d,
			ob.location)
		if loc2d:  # object not behind view origin
			font_id = 0
			blf.position(font_id, loc2d.x + 5, loc2d.y, 0)
			blf.size(font_id, 10, 72)  # 12pt text at 72dpi screen
			blf.draw(font_id, "{l.x:.3f},{l.y:.3f},{l.z:.3f}".format(l=ob.location))

class ShowCoords(bpy.types.Operator):
	bl_idname = 'view3d.showcoords'
	bl_label = 'Show Coords'
	bl_options = {'REGISTER'}

	def modal(self, context, event):
		global running
		if not running:
			self.cancel(context)
			return {'CANCELLED'}
		return {'PASS_THROUGH'}

	def cancel(self, context):
		global handler
		wm = context.window_manager
		if handler:
			bpy.types.SpaceView3D.draw_handler_remove(
				handler, 'WINDOW')
			handler = None
		context.area.tag_redraw()

	def execute(self, context):
		global running
		global handler
		if not running:
			running = True
			args = (context, )
			handler = bpy.types.SpaceView3D.draw_handler_add(
				coords_handler, args, 'WINDOW', 'POST_PIXEL')
			context.window_manager.modal_handler_add(self)
			context.area.tag_redraw()
			return {'RUNNING_MODAL'}
		return {"FINISHED"}

class ShowCoordsEnd(bpy.types.Operator):
	bl_idname = 'view3d.showcoordsend'
	bl_label = 'Hide Coords'
	bl_options = {'REGISTER'}

	def execute(self, context):
		global running
		running = False
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ShowCoords.bl_idname,
		text=ShowCoords.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		ShowCoordsEnd.bl_idname,
		text=ShowCoordsEnd.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	global handler
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	if handler:
		bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
	bpy.utils.unregister_module(__name__)
