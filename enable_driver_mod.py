import bpy

# this script will enable an add-on automatically
# if it is in a text file inside your .blend and
# the name of the text file ends in .py.
# also the Register checkbox should be checked.

def myfunction(x):
	return x*x

bpy.app.driver_namespace["myfunction"] = myfunction
