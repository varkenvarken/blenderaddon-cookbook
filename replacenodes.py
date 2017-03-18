#  replacenodes.py
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
	"name": "Replace nodes",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701061324),
	"blender": (2, 78, 0),
	"location": "Node > Add > Replace nodes",
	"description": "Replace all nodes in the material by a basic node setup",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Experimental development"}

def find_socket(node, name, inputnodes=True):
	"""
	Return all sockets with a given name.
	"""
	found = []
	sockets = node.inputs if inputnodes else node.outputs
	for s in sockets:
		if s.name == name:
			found.append(s)
	return found

class ReplaceNodes(bpy.types.Operator):
	bl_idname = 'mode.replace_nodes'
	bl_label = 'Replace nodes'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return ((context.active_object is not None )
			and (context.scene.render.engine == 'CYCLES'))

	def execute(self, context):
		ob = context.active_object
		slot = ob.material_slots[ob.active_material_index]
		mat = slot.material
		if not mat.use_nodes:
			mat.use_nodes = True

		tree = mat.node_tree
		nodes = tree.nodes
		nodes.clear()

		outputnode = nodes.new('ShaderNodeOutputMaterial') # Node bl_idnames are nowhere documented? But they appear always to be identical with node type names https://www.blender.org/api/blender_python_api_current/bpy.types.ShaderNode.html
		mixnode = nodes.new('ShaderNodeMixShader')
		diffusenode = nodes.new('ShaderNodeBsdfDiffuse')
		specularnode = nodes.new('ShaderNodeBsdfGlossy')

		outputnode.height, outputnode.width = 100,80
		outputnode.location = 300,0
		mixnode.height, mixnode.width = 100,80
		mixnode.location = 100,0
		diffusenode.height, diffusenode.width = 100,80
		diffusenode.location = -100,60
		specularnode.height, specularnode.width = 100,80
		specularnode.location = -100,-60

		links = tree.links

		tos = find_socket(outputnode, 'Surface')[0]
		froms = find_socket(mixnode, 'Shader', False)[0]
		links.new(tos, froms)

		tos = find_socket(mixnode, 'Shader')[0]
		froms = find_socket(diffusenode, 'BSDF', False)[0]
		links.new(tos, froms)

		tos = find_socket(mixnode, 'Shader')[1]
		froms = find_socket(specularnode, 'BSDF', False)[0]
		links.new(tos, froms)

		return {"FINISHED"}


def menu_func(self, context):
	self.layout.operator(
		ReplaceNodes.bl_idname,
		text=ReplaceNodes.bl_label,
		icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)
	bpy.types.NODE_MT_add.append(menu_func)


def unregister():
	bpy.types.NODE_MT_add.remove(menu_func)
	bpy.utils.unregister_module(__name__)
