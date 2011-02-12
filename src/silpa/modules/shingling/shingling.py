#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
# Shingling
#===============================================================================
# Copyright 2011 Hrishikesh K B <hrishi.kb@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
import os,sys
from common import *
from utils import *
from modules import ngram

class Shingling(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'shingling.html')
        self.response  = SilpaResponse(self.template)
        
    @ServiceMethod                            
    def wshingling(self,text, window_size=4):
        window_size=int(window_size)
        s = ngram.getInstance()    
        ngrams=s.wordNgram(text,window_size)
        size=len(ngrams)
        shingling=[]
        for x in ngrams:
            if x not in shingling:
                shingling.append(x)
        return shingling

    def get_module_name(self):
        return "Shingling Library"
    def get_info(self):
        return "Shingling Library for English and Indian languages"    



def getInstance():
    return Shingling()


