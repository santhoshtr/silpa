#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Unicode Character Details
# Copyright 2008-2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# If you find any bugs or have any suggestions email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in
from common import *
import os,sys
from unicodedata import *
class CharDetails(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'chardetails.html')
        self.response = SilpaResponse(self.template)
    
    @ServiceMethod          
    def getdetails(self, text):
        chardetails={}
        for character in text:
            chardetails[character] = {}
            chardetails[character]['Name']= name(character) 
            chardetails[character]['HTML Entity']=str(ord(character)) 
            chardetails[character]['Code point']= repr(character)
            try:
                chardetails[character]['Numeric Value'] = numeric (character)
            except:
                pass    
            try:        
                chardetails[character]['Decimal Value']=decimal (character)
            except:
                pass    
            try:        
                chardetails[character]['Digit']=digit(mychar)
            except:
                pass    
            chardetails[character]['Alphabet']=str(character.isalpha())
            chardetails[character]['Digit']=str(character.isdigit())
            chardetails[character]['AlphaNumeric']=str(character.isalnum())
            chardetails[character]['Canonical Decomposition']=  decomposition(character)
            
        chardetails['Characters'] = list(text)
        return chardetails
    
    def get_module_name(self):
        return "Unicode Character Details"
    def get_info(self):
        return  "Shows the Unicode Character Details of a given character"  
        
def getInstance():
    return CharDetails()

    
