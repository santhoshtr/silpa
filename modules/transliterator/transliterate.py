#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Any Indian Language to any other Indian language transliterator
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
import string
import os
class Transliterator(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'transliterate.html')
    def transliterate_ml_en(self, word):
        virama=u"്"
        #TODO: how to make this more generic so that more languages can be handled here?
        #idea1: transliterate any langauge to a common language say hindi and the n do conversion?
        #existing transliterate.py can be used?
        #idea2: Have dictionaries for each language like english_xx_dict ?
        #TODO: complete this
        english_ml_dict={u'അ':'a',u'ആ':'a',u'ഇ':'a',u'ഈ':'a',u'ഉ':'a',u'ഊ':'a',u'ഋ':'a',\
                u'എ':'a',u'ഏ':'a',u'ഐ':'a',u'ഒ':'a',u'ഓ':'a',u'ഔ':'a',\
                u'ക':'k',u'ഖ':'kh',u'ഗ':'g',u'ഘ':'gh',u'ങ്ങ':'ng',\
                u'ച':'ch',u'ഛ':'chh',u'ജ':'j',u'ഝ':'jhh',u'ഞ':'nj',\
                u'ട':'t',u'ഠ':'th',u'ഡ':'d',u'ഢ':'dh',u'ണ':'n',\
                u'ത':'th',u'ഥ':'th',u'ദ':'d',u'ധ':'dh',u'ന':'n',\
                u'പ':'p',u'ഫ':'ph',u'ബ':'b',u'ഭ':'bh',u'മ':'m',\
                u'യ':'y',u'ര':'r',u'ല':'l', u'വ':'v', u'റ':'r',\
                u'ശ':'sa',u'ഷ':'sh',u'സ':'s', u'ഹ':'h',u'ള':'l',u'ഴ':'zh',\
                u'ാ':'a',u'ി':'i' ,u'ീ':'ee' ,u'ു':'u',\
                u'ൂ':'uu',u'ൃ':'ri' ,u'െ':'e' ,u'േ':'e',\
                u'ൈ':'ai',u'ൊ':'o' ,u'ോ':'oo' ,u'ൗ':'au'}
        word_length =len(word)
        index=0
        tx_string=""
        while index<word_length:
            a_vowel=""
            try:
                if(index+1<word_length):
                    if(word[index+1]==virama):
                        a_vowel=""      
                else:
                    if(index+1<word_length):
                        if (english_ml_dict[word[index+1]] in ['a','e','i','o','u']):
                            a_vowel=""              
                    else:   
                        a_vowel="a"     
                    if (english_ml_dict[word[index]] in ['a','e','i','o','u']): 
                        a_vowel=""              
                    tx_string=tx_string+ english_ml_dict[word[index]] + a_vowel
            except:     
                tx_string=tx_string+ word[index]
            index=index+1   
        return  tx_string
    def _malayalam_fixes(self, text):
        text = text.replace(u"മ് ",u"ം ")
        text = text.replace(u"മ്,",u"ം,")
        text = text.replace(u"മ്.",u"ം.")
        text = text.replace(u"മ്)",u"ം)")
        text = text.replace(u"ഩ",u"ന")          
        text = text.replace(u"൤",u".")   #danda by fullstop
        return text 
        
    @ServiceMethod
    def transliterate(self,text, target_lang_code):
        text =  normalize(text)
        tx_str=""
        words=text.split(" ")
        for word in words:
            if(word.strip()>""):
                try:
                    src_lang_code=detect_lang(word)[word]
                except:
                    tx_str = tx_str + " " + word 
                    continue #FIXME 
                if((target_lang_code=="en_US") and (src_lang_code=="ml_IN")):
                    tx_str=tx_str + self.transliterate_ml_en(word)
                    continue    
                for chr in word:
                    if chr in string.punctuation or chr<='z':
                        tx_str = tx_str + chr 
                        continue
                    offset = ord(chr) + self.getOffset(src_lang_code, target_lang_code) 
                    if(offset>0):
                        tx_str = tx_str + unichr (offset) 
                tx_str = tx_str   + " "
            else:
                tx_str = tx_str   +  word
        # Language specific fixes
        if target_lang_code == "ml_IN":
            tx_str = self._malayalam_fixes(tx_str)      
        return  tx_str

    def getOffset(self,src,target):
        lang_bases={'en_US':0,'hi_IN': 0x0901,'bn_IN': 0x0981, 'pa_IN':0x0A01,'gu_IN':0x0A81 , 'or_IN': 0x0B01,'ta_IN': 0x0B81,'te_IN' : 0x0C01,    'kn_IN' :0x0C81 ,'ml_IN': 0x0D01}
        src_id=0
        target_id=0
        try:
            src_id=lang_bases[src]
            target_id=lang_bases[target]
            return (target_id - src_id)
        except:
            return 0    

    def get_module_name(self):
        return "Transliterator"
    def get_info(self):
        return  "Transliterated the text between any Indian Language"   
        
        
def getInstance():
    return Transliterator()     
        
