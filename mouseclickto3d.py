#  mouseclickto3d.py
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
from bpy_extras import view3d_utils

bl_info = {
	"name": "Mouseclick 3D",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701081101),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Point 3D",
	"description": "Determine 3D world location of mouse click",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

class Mouseclick3D(bpy.types.Operator):
	bl_idname = 'scene.mouseclick3d'
	bl_label = 'Point 3D'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def get_3d_point(self, context, event):
		"""
		Return the point in 3D space for the mouse coords
		"""
		# get the context arguments
		scene = context.scene
		region = context.region
		rv3d = context.region_data
		coord = event.mouse_region_x, event.mouse_region_y

		# get the ray from the viewport and mouse
		view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
		ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
		#ray_target = ray_origin + view_vector

		result, location, normal, index, obj, matrix = scene.ray_cast(ray_origin, view_vector)

		return result, location

	def modal(self, context, event):

		if event.type in {'RIGHTMOUSE', 'ESC'}:
			context.area.header_text_set()
			context.area.tag_redraw()
			return {'CANCELLED'}
		elif (event.type == 'LEFTMOUSE'
				and event.value == 'RELEASE'):
			hit, location = self.get_3d_point(context, event)
			if hit:
				context.area.header_text_set(
					"Location: {l.x:.2f},{l.y:.2f},{l.z:.2f}".format(l=location))
			else:
				context.area.header_text_set("Location: no hit")
		context.area.tag_redraw()

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(
		Mouseclick3D.bl_idname,
		text=Mouseclick3D.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
