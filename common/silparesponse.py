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

class SilpaResponse:
    def __init__(self):
        xhtml = getTemplate()
        self.page = Meld(xhtml)     
        
    def toString(self):
        return str(self.page)

    def set_form(self,value):
        if(value):
            self.page.form = value

    def set_result(self,value):
        if(value):
            self.page.result= value 

    def set_error_message(self,value):
        if(value):
            self.page.errormessage = value

    def set_success_message(self,value):
        if(value):
            self.page.successmessage = value

    def set_content(self, value):
        if value:
            self.page.content = value           

    def set_footer(self, value):
        if value:
            self.page.footer = value
        
