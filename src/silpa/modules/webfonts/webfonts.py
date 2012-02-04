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
from utils import *
from common.silparesponse import SilpaResponse
import fonts

class Webfonts(SilpaModule):
    def __init__(self):
        self.template = os.path.join(os.path.dirname(__file__), 'index.html')  
        self.font = None
        #List of available fonts
        self.available_fonts=fonts.fonts
        self.response = SilpaResponse(self.template)
        
    def set_request(self,request):
        self.request = request
        self.font = self.request.get('font')

    def set_start_response(self,start_response):
        self.start_response = start_response
        
            
    def get_response(self):
        if self.font:
            css =  self.serve(self.font)
            self.response.content = css
            self.response.response_code = "200 OK" 
            self.response.header  = [('Content-Type', 'text/css'),('Access-Control-Allow-Origin','*')]
        return self.response
                
    def serve(self,font=None):
        """
        serve the font file
        """
            
        """
        Provide the css for the given font.
        """     

        if not self.available_fonts.has_key(self.font):
            return "Error!, Font not available"
        http_host =self.request.get('HTTP_HOST')
        request_uri =self.request.get('REQUEST_URI')

        silpalogger.debug("Request URI "+request_uri)

        if request_uri != None:
            http_host += "/"+get_base_url()

        font_url = "http://"+http_host+"/modules/webfonts/font/"
        css = '''@font-face {
            font-family: '$$FONTFAMILY$$';
            src: url('$$FONTURLEOT$$');
            src: local('☺'), url('$$FONTURLWOFF$$') format('woff'), url('$$FONTURLTTF$$') format('truetype');
            font-weight: normal;
            font-style: normal;
        }
        '''
        css = css.replace("$$FONTURLEOT$$",font_url + self.available_fonts[self.font]['eot'])
        css = css.replace("$$FONTURLWOFF$$",font_url + self.available_fonts[self.font]['woff'])
        css = css.replace("$$FONTURLTTF$$",font_url + self.available_fonts[self.font]['ttf'])
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
