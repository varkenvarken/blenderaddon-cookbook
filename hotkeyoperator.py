import bpy
from random import random

bl_info = {
	"name": "Dummy Operator with hot key",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701150933),
	"blender": (2, 78, 0),
	"location": "View3D > Object > Dummy Op",
	"description": "A dummy operator with a hot key",
	"category": "Experimental development"}


class HotkeyDummyOp(bpy.types.Operator):
	bl_idname = 'object.hotkeydummyop'
	bl_label = 'Dummy Op'
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(self, context):
		return (context.mode == 'OBJECT')

	def execute(self, context):
		# move the active object in a random direction
		if context.active_object:
			loc = context.active_object.location
			loc.x += (random() - 0.5)
			loc.y += (random() - 0.5)
			loc.z += (random() - 0.5)
		return {"FINISHED"}

def menu_func(self, context):
	self.layout.operator(
		HotkeyDummyOp.bl_idname,
		text=HotkeyDummyOp.bl_label,
		icon='PLUGIN')

# not used, but you can dump a list of mapnames with this fie
def dump_mapnames():
	names = set()
	for kc in C.window_manager.keyconfigs.values():
		for km in kc.keymaps.values():
			names.add(km.name)
	print(sorted(names))

km = None
ki = None

def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_object.append(menu_func)

	wm = bpy.context.window_manager
	kc = wm.keyconfigs

	global km
	global ki
	mapname = 'Object Non-modal'
	if mapname in kc.addon.keymaps:
		km = kc.addon.keymaps[mapname]
	else:
		km = kc.addon.keymaps.new(mapname)
	ki = km.keymap_items.new(HotkeyDummyOp.bl_idname, 'BACK_SLASH', 'PRESS', head=True)


def unregister():

	global km
	global ki
	if km and ki:
		km.keymap_items.remove(ki)

	bpy.types.VIEW3D_MT_object.remove(menu_func)
	bpy.utils.unregister_module(__name__)
# even though we unregister stuff in the right order we still get some (harmless) warnings in the console:
# "search for unknown operator 'OBJECT_OT_hotkeydummyop', 'OBJECT_OT_hotkeydummyop'"
# see:
# https://blenderartists.org/forum/showthread.php?328943-Hotkey-uninstall-issue-Search-for-unknown-operator

