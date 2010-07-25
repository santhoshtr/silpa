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
import codecs
from common import *
from utils import *

class Webfonts(SilpaModule):
    def __init__(self):
        self.template = os.path.join(os.path.dirname(__file__), 'index.html')  
        self.font=None

        #List of available fonts
        self.available_fonts=['Meera','Rachana', 'Suruma', 'AnjaliOldLipi',
                              'Kalyani','RaghuMalayalam','LohitMalayalam',
                              'Dyuthi','Malige','Kedage','LohitKannada']

        # Generate path for the font information file
        self.font_info_file = os.path.join(os.path.dirname(__file__),"fonts.info")

        # Read the entire file so this will be invoked only
        # first time
        # P.S don't use unicode() function here it will mess
        # up everything
        self.font_info_lines = codecs.open(self.font_info_file,encoding="utf-8",errors="ignore").read().split("\n")
        
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
        http_host =self.request.get('HTTP_HOST')
        request_uri =self.request.get('REQUEST_URI')
        if request_uri!=None:
            http_host+="/silpa"
        if self.font not in self.available_fonts:
            return "Error!, Font not available"
        user_agent= self.request.get('HTTP_USER_AGENT')
        if user_agent.find("MSIE")<0:
            css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src: local('$$FONTFAMILY$$'), url('$$FONTURL$$') format('truetype');}"
            css=css.replace('$$FONTURL$$', "http://"+http_host +'/modules/webfonts/font/' + self.font + '.ttf')
        else:
            css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src:local('$$FONTFAMILY$$'), url('$$FONTURL$$');}"
            css=css.replace('$$FONTURL$$', "http://"+http_host +'/modules/webfonts/font/' + self.font + '.eot')

        css=css.replace('$$FONTFAMILY$$',self.font)
        return css
        
   
    
    @ServiceMethod      
    def get_fonts_list(self, language=None):
        """
        return a list of available fonts names for the given Language
        If the language is not given, return all the available fonts
        """

        # Font map which holds details
        font_map = {}
        for line in self.font_info_lines:
            # TODO: For each line create new map object This is weird
            # but for some reason same object reference was used
            # by Python so all Fonts will have same value as last
            # font updated but it was working fine in chardetails
            # module need to check on this
            
            details_map = {}
            
            # If the line starts with # its comment just skip it
            if line.startswith("#"):
                continue
            # Split the line on ","
            info = line.split(",")

            # If there are less than 3 objects this is not a valid line
            # and can cause trouble in further processing so skip it
            
            if len(info) < 3:
                continue

            try:
                details_map["Language"] = info[1]
                details_map["SampleText"] = info[2]
                font_map[info[0]] = details_map
            except:
                silpalogger.debug(info)
                silpalogger.exception("Index out of bound exeption")

        #use this for debugging only don't log real data
        # silpalogger.debug(font_map) 

        # Ok now add list of available fonts which will be used by client
        # as key to get details of each font
        font_map["Fonts"] = self.available_fonts
        return font_map
            
            
        
        
        
    def get_module_name(self):
        return "Webfonts"
        
    def get_info(self):
        return  "Indic Webfonts"   
        
def getInstance():
    return Webfonts()
