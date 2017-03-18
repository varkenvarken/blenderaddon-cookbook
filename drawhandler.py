#  drawhandler.py
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
from bpy.props import BoolProperty
import bgl
import blf
from time import localtime, strftime
from math import sin,cos

bl_info = {
	"name": "Draw Handler",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201703121240),
	"blender": (2, 78, 0),
	"location": "View3D > View > Show clock",
	"description": "Install a clock",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

running = False
handler = None
timer = None

ticks = [(sin(6.283 * t/12.0), cos(6.283 * t/12.0)) for t in range(12)]

buf = bgl.Buffer(bgl.GL_INT, 4)  # linear array of 4 ints

def cursor_handler(context):

	global ticks
	global buf

	bgl.glGetIntegerv(bgl.GL_VIEWPORT,buf)
	width = buf[2]

	t = localtime()
	m = t[4]
	h = (t[3]%12) + m/60.0  # fractional hours
	twopi = 6.283

	# draw text
	font_id = 0
	blf.position(font_id, width - 100, 15, 0)
	blf.size(font_id, 12, 72)  # 12pt text at 72dpi screen
	blf.draw(font_id, strftime("%H:%M:%S", t))

	# 50% alpha, 2 pixel lines
	bgl.glEnable(bgl.GL_BLEND)
	bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
	bgl.glLineWidth(2)

	# draw a clock in the lower right hand corner
	startx, starty = (width - 22.0,22.0)
	smallhandx, smallhandy = (startx + 9*sin(twopi * h/12),
							starty + 9*cos(twopi * h/12))
	bighandx, bighandy = (startx + 15*sin(twopi * m/60),
							starty + 15*cos(twopi * m/60))
	bgl.glBegin(bgl.GL_LINES)
	bgl.glVertex2f(startx, starty)
	bgl.glVertex2f(bighandx, bighandy)
	bgl.glVertex2f(startx, starty)
	bgl.glVertex2f(smallhandx, smallhandy)
	# twelve small dots
	for x,y in ticks:
		bgl.glVertex2f(startx + 17*x, starty + 17*y)
		bgl.glVertex2f(startx + 18*x, starty + 18*y)
	bgl.glEnd()

	# restore opengl defaults
	bgl.glLineWidth(1)
	bgl.glDisable(bgl.GL_BLEND)
	bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

# also see http://blender.stackexchange.com/questions/30295/how-add-properties-to-operator-modal-draw

class ModalDrawHandlerOp(bpy.types.Operator):
	bl_idname = 'view3d.modaldrawhandlerop'
	bl_label = 'Show Clock'
	bl_options = {'REGISTER'}

	def modal(self, context, event):
		global running
		global width
		if not running:
			self.cancel(context)
			return {'CANCELLED'}
		if event.type == 'TIMER':
			context.area.tag_redraw()  # yes this is needed
		return {'PASS_THROUGH'}

	def cancel(self, context):
		global timer
		global handler
		wm = context.window_manager
		if timer:
			wm.event_timer_remove(timer)
			print('timer removed')
		if handler:
			bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
			handler = None  # prevent error on unregister()
			print('handler removed')
		context.area.tag_redraw()

	def execute(self, context):
		global running
		global handler
		global timer
		if not running:
			running = True
			args = (context, )
			handler = bpy.types.SpaceView3D.draw_handler_add(cursor_handler, args, 'WINDOW', 'POST_PIXEL')
			timer = context.window_manager.event_timer_add(1.0, context.window)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {"FINISHED"}

class DrawHandlerOp(bpy.types.Operator):
	bl_idname = 'view3d.drawhandlerop'
	bl_label = 'Hide Clock'
	bl_options = {'REGISTER'}

	def execute(self, context):
		global running
		running = False
		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ModalDrawHandlerOp.bl_idname,
		text=ModalDrawHandlerOp.bl_label,
		icon='PLUGIN')
	self.layout.operator(
		DrawHandlerOp.bl_idname,
		text=DrawHandlerOp.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
	global handler
	bpy.types.VIEW3D_MT_view.remove(menu_func)
	if handler:
		bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
	bpy.utils.unregister_module(__name__)
