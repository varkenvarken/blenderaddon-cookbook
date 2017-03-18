#  drivers.py
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
