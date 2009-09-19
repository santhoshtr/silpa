#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Katapayadi
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
from utils import *
import os
class Katapayadi(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'katapayadi.html')
    
    @ServiceMethod
    def get_number(self, word):
        word = word.strip()
        word = word.split(" ")[0]
        lang_ka_bases = {'hi_IN': 0x0915,'bn_IN': 0x0995, 'pa_IN':0x0A15,'gu_IN':0x0A95 , 'or_IN': 0x0B15,'ta_IN': 0x0B95,'te_IN' : 0x0C15,    'ka_IN' :0x0C95 ,'ml_IN': 0x0D15}        
        from modules import syllabalizer
        syllablizer_handle = syllabalizer.getInstance()
        syllables = syllablizer_handle.syllabalize(word)
        number = ""
        src_lang_code = detect_lang(word)[word]
        base =  lang_ka_bases[src_lang_code]
        for cluster in syllables:
            number = self.__get_number_for_syllable(cluster,base)  + number 
        return  int(number)
        
    def __get_number_for_syllable(self, syllable,base):
       
        katapayadi = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,0,1,2,3,4,5,1,2,0,3,9,0,4,5,6,7,8]
        length= len(syllable)
        index = length -1 
        
        while index >= 0 :
            chr = syllable[index]
            offset=ord(chr) - base
            
            if offset >= 0 : 
                try:
                    return str(katapayadi[offset])
                except:
                    pass
            index -= 1          
        return "0"
    @ServiceMethod              
    def get_swarasthanas(self, raga):
        swarasthans = ["Sa"]
        try:
            number = int(str(raga))
        except:       
            number = self. get_number(raga)
            if number < 99 : return "Could not recognize the raga"
        melakartha_number = number%100
        quotient = (melakartha_number-1)/6
        remainder = (melakartha_number-1)%6
        quotient = quotient%6
        if quotient == 0 : 
            swarasthans.append("Ri1")
            swarasthans.append("Ga1")
        if quotient == 1 : 
            swarasthans.append("Ri1")
            swarasthans.append("Ga2")
        if quotient == 2 : 
            swarasthans.append("Ri1")
            swarasthans.append("Ga3")
        if quotient == 3 : 
            swarasthans.append("Ri2")
            swarasthans.append("Ga2")
        if quotient == 4 : 
            swarasthans.append("Ri2")
            swarasthans.append("Ga3")
        if quotient == 5 : 
            swarasthans.append("Ri3")
            swarasthans.append("Ga3")                  
        if  melakartha_number <= 36 :
            swarasthans.append("Ma1")                
        if  melakartha_number > 36 and melakartha_number <= 72:
            swarasthans.append("Ma2")                    
        swarasthans.append("Pa")                         
        if remainder == 0 : 
            swarasthans.append("Da1")
            swarasthans.append("Ni1")                  
        if remainder == 1 : 
            swarasthans.append("Da1")
            swarasthans.append("Ni2")                  
        if remainder == 2 : 
            swarasthans.append("Da1")
            swarasthans.append("Ni3")                  
        if remainder == 3 : 
            swarasthans.append("Da2")
            swarasthans.append("Ni2")                  
        if remainder == 4 : 
            swarasthans.append("Da2")
            swarasthans.append("Ni3")                  
        if remainder == 5 : 
            swarasthans.append("Da3")
            swarasthans.append("Ni3")                                      
        swarasthans.append("Sa")                  
        return dumps(swarasthans)
    def get_module_name(self):
        return "Katapayadi Number System"
    def get_info(self):
        return  "Decodes the numbers from the katapayadi numbering system"  

def getInstance():
    return Katapayadi()     

    
