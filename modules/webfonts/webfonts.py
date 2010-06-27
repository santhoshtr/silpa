#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import cgitb
import os
import cgi
import sys
from common import *

class Webfonts(SilpaModule):
    def __init__(self):
        self.template = os.path.join(os.path.dirname(__file__), 'index.html')  
        self.font=None
        self.available_fonts=['Meera','Rachana', 'Suruma', 'AnjaliOldLipi', 'Kalyani','RaghuMalayalam','Lohit Malayalam','Dyuthi','Mallige-n','Kedage-n','lohit_kn']
        
    def set_request(self,request):
        self.request=request
        self.font = self.request.get('font')
        
    def is_self_serve(self) :       
        if self.font:
            return True
        else:
            return False
            
    def get_mimetype(self):
        return "text/css"
        
    def serve(self,font=None):
        """
        Provide the css for the given font. CSS will differ for IE and Other browsers
        """
        http_ref =self.request.get('HTTP_REFERER')
        http_ref=http_ref.replace("Webfonts","")
        if self.font not in self.available_fonts:
            return "Error!, Font not available"
        user_agent= self.request.get('HTTP_USER_AGENT')
        if user_agent.find("MSIE")<0:
            css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src: local('$$FONTFAMILY$$'), url('$$FONTURL$$') format('truetype');}"
            css=css.replace('$$FONTURL$$', http_ref +'/modules/webfonts/font/' + self.font + '.ttf')
        else:
            css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src:local('$$FONTFAMILY$$'), url('$$FONTURL$$');}"
            css=css.replace('$$FONTURL$$', http_ref +'/modules/webfonts/font/' + self.font + '.eot')

        css=css.replace('$$FONTFAMILY$$',self.font)
        return css
    
    @ServiceMethod      
    def get_fonts_list(self, language=None):
        """
        return a list of available fonts names for the given Language
        If the language is not given, return all the available fonts
        """
        return self.available_fonts
        
    def get_module_name(self):
        return "Webfonts"
        
    def get_info(self):
        return  "Indic Webfonts"   
        
def getInstance():
    return Webfonts()
        
