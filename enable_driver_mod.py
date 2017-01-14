import bpy

# this script will enable an add-on automatically 
# if it is in a text file inside your .blend and
# the name of the text file ends in .py.
# also the Register checkbox should be checked.

#from time import time
# in this case we enable the add-on drivers.py

#bpy.ops.wm.addon_disable(module="drivers")
#bpy.ops.wm.addon_enable(module="drivers")

#print("text buffer",time())

#print(bpy.app.driver_namespace["myfunction"])

#for ob in bpy.data.objects:
#    if ob.animation_data:
#        for fcurve in ob.animation_data.drivers:
#            fcurve.driver.expression += ''

def myfunction(x):
	return x*x

bpy.app.driver_namespace["myfunction"] = myfunction