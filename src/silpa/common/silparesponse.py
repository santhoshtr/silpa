# -*- coding: utf-8 -*-
# Copyright 2009-2010
# Santhosh Thottingal <santhosh.thottingal@gmail.com>
# This code is part of Silpa project.
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
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from utils import *
from PyMeld import Meld

class SilpaResponse():
    
    def __init__(self, content_template=None):
        self.content = Meld(get_template())
        if content_template:
            self.content.form = open(content_template,'r').read()
        self.mime_type = 'text/html'
        self.response_code = "200 OK"
        self.header = [('Content-Type', self.mime_type)]
        
    def get_mimetype(self):
        return self.mime_type
        
    def get_header(self):
        return self.header

    def set_mimetype(self, mime_type): 
        self.mime_type = mime_type
        
    def populate_form(self,request):
        #try to populate the html form with the values from the request.
        if request == None:
            return 
        for key in request:
            try:
                value = request.get(key)
                field = self.content.__getattr__(key)
                field.value = value
                self.content.__getattr__(value).selected= 'selected' 
            except:
                pass
        return self   
        
     
        
