# -*- coding: utf-8 -*-
# UCA Collation
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
import os
from common import *
from utils import *
from pyuca import Collator 
class Sort(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), "sort.html")
        self.silpacollator = Collator(os.path.join(os.path.dirname(__file__), "allkeys-5.2-silpa.txt"))
        self.ucacollator = Collator(os.path.join(os.path.dirname(__file__), "allkeys-5.2.txt"))
        
    @ServiceMethod  
    def sort(self, text):
        words = text.split()
        sorted_words= {}
        sorted_words['SILPA'] = sorted(words, key=self.silpacollator.sort_key) 
        sorted_words['UCA'] = sorted(words, key=self.ucacollator.sort_key) 
        return dumps(sorted_words)

    def get_module_name(self):
        return "Sort"
    def get_info(self):
        return  "Sorts a set of words linguistically."  

def getInstance():
    return Sort()
        
