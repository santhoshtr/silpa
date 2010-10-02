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
import fonts
class Webfonts(SilpaModule):
    def __init__(self):
        self.template = os.path.join(os.path.dirname(__file__), 'index.html')  
        self.font=None

        #List of available fonts
        self.available_fonts=fonts.fonts
        
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
            
        if not self.available_fonts.has_key(self.font):
            return "Error!, Font not available"
        user_agent= self.request.get('HTTP_USER_AGENT')
        print user_agent
        if user_agent.find("MSIE")>0:
            css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src:local('$$FONTFAMILY$$'), url('$$FONTURL$$');}"
            css=css.replace('$$FONTURL$$', "http://"+http_host +'/modules/webfonts/font/' + self.available_fonts[self.font]['eot'])    
        else:
            if user_agent.find("Chrome")>0:    
                css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src: local('$$FONTFAMILY$$'), url('$$FONTURL$$') format('woff');}"
                css=css.replace('$$FONTURL$$', "http://"+http_host +'/modules/webfonts/font/' +  self.available_fonts[self.font]['woff'])
            else:
                css = "@font-face {font-family: '$$FONTFAMILY$$';font-style: normal;font-weight: normal;src: local('$$FONTFAMILY$$'), url('$$FONTURL$$') format('truetype');}"
                css=css.replace('$$FONTURL$$', "http://"+http_host +'/modules/webfonts/font/' +  self.available_fonts[self.font]['ttf'])    

        css=css.replace('$$FONTFAMILY$$',self.font)
        return css
        
   
    
    @ServiceMethod      
    def get_fonts_list(self, languages=[]):
        """
        return a list of available fonts names for the given Language
        """
        results = []
        if languages==[]:
            return results
        else:
            for language in languages:
				try:
					for font in self.available_fonts:
						if self.available_fonts[font]['Language']  == language:
							results.append({font:self.available_fonts[font]})
				except KeyError:
					pass    
        return results    
        
    def get_module_name(self):
        return "Webfonts"
        
    def get_info(self):
        return  "Indic Webfonts"   
        
def getInstance():
    return Webfonts()
