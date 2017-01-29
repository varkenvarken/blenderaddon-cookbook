import bpy

# you can use this as an add-on but then before your drivers
# will work you have to enable it. A better option is to
# copy this into a text buffer in the text editor and check
# the register checkbox. See enable_driver_mod.py

bl_info = {
	"name": "Dummy Operator",
	"author": "Michel Anders (varkenvarken)",
	"version": (0, 0, 201701141335),
	"blender": (2, 78, 0),
	"location": "None: this add-on provides driver functions",
	"description": "Provides the driver 'myfunction'",
	"category": "Experimental development"}

def myfunction(x):
	return x*x

def register():
	bpy.app.driver_namespace["myfunction"] = myfunction

def unregister():
	pass
