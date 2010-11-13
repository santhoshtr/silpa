#!/usr/bin/python
# -*- coding: utf-8 -*-
#styles.py
#      
#Copyright 2010 Vasudev Kamath <kamathvasudev@gmail.com>
#      
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU  General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#     
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#      
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.
#

class Color(object):
	def __init__ (self,red, green, blue, alpha=1.0):
            	self.red = red
		self.green = green
		self.blue = blue
		self.alpha = alpha
__colors = {
    "Black": Color(0,0,0),
    "Blue": Color(0,0,255),
    "Red": Color(255,0,0),
    "Green": Color(0,255,0),
    "Yellow": Color(255,255,0)
    }

def get_color(name="Black"):
    return __colors.get(name,"Black")
