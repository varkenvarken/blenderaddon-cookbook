#  customproperty.py
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
from bpy.props import IntProperty, BoolProperty, FloatProperty
from math import sin,cos,pi

bl_info = {
	"name": "Add a star object",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701151447),
	"blender": (2, 78, 0),
	"location": "View3D > Add > Mesh > Star",
	"description": "Add a star object with custom object properties",
	"category": "Experimental development"}

def updateStar(self, context):
	ob = context.active_object
	mesh = ob.data
	bm = bmesh.new()
	angle = 2 * pi / ob.star.points  # property of ob, not operator!
	minr = ob.star.minradius
	maxr = ob.star.maxradius
	for p in range(ob.star.points):
		s = p * angle
		bm.verts.new((minr * cos(s), minr * sin(s), 0))
		s += angle/2
		bm.verts.new((maxr * cos(s), maxr * sin(s), 0))
	bm.faces.new(bm.verts)  # all newly added faces
	bm.to_mesh(mesh)
	bm.free()

class StarPropertyGroup(bpy.types.PropertyGroup):
	isstar = BoolProperty(name="Star", default=False)
	points = IntProperty(name="Points",
					default=5, min=3, update=updateStar)
	minradius = FloatProperty(name="Minimum r",
					default=0.5, min=0, update=updateStar)
	maxradius = FloatProperty(name="Maximum r",
					default=1, min=0, update=updateStar)

class StarOp(bpy.types.Operator):
	bl_idname = 'mesh.starop'
	bl_label = 'Star'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		bpy.ops.mesh.primitive_cube_add()
		context.active_object.name = "Star"
		props = context.active_object.star
		props.star = True
		updateStar(self, context)
		return {"FINISHED"}

class StarPanel(bpy.types.Panel):
	bl_label = "Star"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Star"
	bl_options = set()

	@classmethod
	def poll(self, context):
		# Check if we are in object mode and dealing with a star object)
		return ((context.mode == 'OBJECT')
				and (context.active_object is not None)
				and (context.active_object.star.star))

	def draw(self, context):
		layout = self.layout
		props = context.active_object.star
		layout.prop(props, 'points')
		layout.prop(props, 'minradius')
		layout.prop(props, 'maxradius')

def menu_func(self, context):
	self.layout.operator(
		StarOp.bl_idname,
		text=StarOp.bl_label,
		icon='PLUGIN')

def register():
	bpy.utils.register_module(__name__)
	bpy.types.Object.star = bpy.props.PointerProperty(type=StarPropertyGroup)
	bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
	bpy.types.INFO_MT_mesh_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)

