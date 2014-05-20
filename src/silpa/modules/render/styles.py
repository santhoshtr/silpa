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
    "black": Color(0,0,0),
    "blue": Color(0,0,1),
    "red": Color(1,0,0),
    "green": Color(0,1,0),
    "yellow": Color(1,1,0)
    }

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    hex_len = len(hex_value)
    if hex_len != 6 and hex_len != 8:
        return __colors.get("black")
    else:
        r, g, b = hex_value[:2], hex_value[2:4], hex_value[4:6]
        if hex_len == 8:
            a = hex_value[6:8]
        else:
            a = 'ff'
        try:
            r, g, b, a = [int(n, 16) for n in (r, g, b, a)]
            return Color(round(float(r)/255, 2),round(float(g)/255, 2),round(float(b)/255, 2), round(float(a)/255, 2))
        except:
            return __colors.get("black")

def get_color(name="black"):
    if name.startswith('#'):
        return hex_to_rgb(name)
    else:
        return __colors.get(name.lower(),__colors.get("black"))

