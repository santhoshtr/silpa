#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Any Indian Language to any other Indian language transliterator
# Copyright 2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
from cmudict import CMUDict

class Transliterator(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'transliterate.html')
        self.cmu = CMUDict()
    def transliterate_en_ml(self, word):   
        return self.cmu.pronunciation(word,"ml_IN")
    def transliterate_iso15919(self, word, src_language):
        tx_str = ""
        index=0;
        word_length = len(word)
        for chr in word:
            index+=1
            offset = ord(chr) - lang_bases[src_language]
            #76 is the virama offset for all indian languages from its base
            if offset >= 61  and offset <=76: 
			    tx_str = tx_str[:-1] #remove the last 'a' 
            if offset>0 and offset<=128:
                tx_str = tx_str + charmap["ISO15919"][offset]
            #delete the inherent 'a' at the end of the word from hindi    
            if tx_str[-1:]=='a' and (src_language == "hi_IN" or src_language == "gu_IN" or src_language == "bn_IN" ) :
				if word_length ==  index and word_length>1: #if last letter 
				    tx_str = tx_str[:-1] #remove the last 'a' 
        return tx_str .decode("utf-8")
    def transliterate_ipa(self, word, src_language):
        tx_str = ""
        index=0;
        word_length = len(word)
        for chr in word:
            index+=1
            offset = ord(chr) - lang_bases[src_language]
            #76 is the virama offset for all indian languages from its base
            if offset >= 61  and offset <=76: 
			    tx_str = tx_str[:-(len('ə'))] #remove the last 'ə' 
            if offset>0 and offset<=128:
                tx_str = tx_str + charmap["IPA"][offset]
            #delete the inherent 'a' at the end of the word from hindi    
            if tx_str[-1:]=='ə' and (src_language == "hi_IN" or src_language == "gu_IN" or src_language == "bn_IN" ) :
				if word_length ==  index and word_length>1: #if last letter 
				    tx_str = tx_str[:-(len('ə'))] #remove the last 'a' 
        return tx_str .decode("utf-8")
    def transliterate_ml_en(self, word):
        virama=u"്"
        #TODO: how to make this more generic so that more languages can be handled here?
        #idea1: transliterate any langauge to a common language say hindi and the n do conversion?
        #existing transliterate.py can be used?
        #idea2: Have dictionaries for each language like english_xx_dict ?
        #TODO: complete this
        malayalam_english_dict={u'അ':'a',u'ആ':'aa',u'ഇ':'i',u'ഈ':'ee',u'ഉ':'u',u'ഊ':'oo',u'ഋ':'ri',\
                u'എ':'e',u'ഏ':'e',u'ഐ':'ai',u'ഒ':'o',u'ഓ':'o',u'ഔ':'au',\
                u'ക':'k',u'ഖ':'kh',u'ഗ':'g',u'ഘ':'gh',u'ങ്ങ':'ng',u'ങ':'ng',\
                u'ച':'ch',u'ഛ':'chh',u'ജ':'j',u'ഝ':'jhh',u'ഞ':'nj',\
                u'ട':'t',u'ഠ':'th',u'ഡ':'d',u'ഢ':'dh',u'ണ':'n',\
                u'ത':'th',u'ഥ':'th',u'ദ':'d',u'ധ':'dh',u'ന':'n',\
                u'പ':'p',u'ഫ':'ph',u'ബ':'b',u'ഭ':'bh',u'മ':'m',\
                u'യ':'y',u'ര':'r',u'ല':'l', u'വ':'v', u'റ':'r',\
                u'ശ':'s',u'ഷ':'sh',u'സ':'s', u'ഹ':'h',u'ള':'l',u'ഴ':'zh',\
                u'്':'',u'ം':'m',u'ാ':'aa',u'ി':'i' ,u'ീ':'ee' ,u'ു':'u',\
                u'ൂ':'oo',u'ൃ':'ri' ,u'െ':'e' ,u'േ':'e',\
                u'ൈ':'ai',u'ൊ':'o' ,u'ോ':'oo' ,u'ൗ':'au',  u'ൌ':'ou'}
        ml_vowels = [u'അ',u'ആ',u'ഇ',u'ഈ',u'ഉ' ,u'ഊ',u'ഋ', u'എ',u'ഏ',u'ഐ',u'ഒ',u'ഓ',u'ഔ']                        
        ml_vowel_signs = [u'്',u'ം',u'ാ',u'ി',u'ീ',u'ു', u'ൂ',u'ൃ' ,u'െ' ,u'േ',u'ൈ',u'ൊ' ,u'ോ' ,u'ൗ' , u'ൌ',u'‍']        
        word_length = len(word)
        index = 0
        tx_string = ""
        while index < word_length:
            if word[index] == u'്':
                index+=1
                continue;
            try:
                tx_string += malayalam_english_dict[word[index]]
            except KeyError:
                tx_string += word[index]
            if index+1 < word_length and not word[index+1] in ml_vowel_signs and word[index+1] in malayalam_english_dict and not word[index] in ml_vowels and not word[index] in ml_vowel_signs :
                tx_string +='a'
            if index+1 == word_length and not word[index] in ml_vowel_signs and word[index] in malayalam_english_dict:
                tx_string +='a'
            #handle am sign
            if index+1 < word_length and word[index+1] == u'ം' and  not word[index] in ml_vowel_signs:
				tx_string +='a'
            index+=1
        return tx_string       
    def _malayalam_fixes(self, text):
        try:
            text = text.replace(u"മ് ",u"ം ")
            text = text.replace(u"മ്,",u"ം,")
            text = text.replace(u"മ്.",u"ം.")
            text = text.replace(u"മ്)",u"ം)")
            text = text.replace(u"ഩ",u"ന")          
            text = text.replace(u"൤",u".")   #danda by fullstop
        except:
            pass    
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
                if src_lang_code=="en_US" :    
                    if target_lang_code=="ml_IN" :
                        tx_str=tx_str + self.transliterate_en_ml(word)   + " "
                        continue
                    else:    
                        tx_str="Not implemented now."
                        break    
                if target_lang_code=="ISO15919" :
                    tx_str=tx_str + self.transliterate_iso15919(word, src_lang_code)   + " "
                    continue
                if target_lang_code=="IPA" :
                    tx_str=tx_str + self.transliterate_ipa(word, src_lang_code)   + " "
                    continue
                if target_lang_code=="en_US" :
                    if src_lang_code=="ml_IN" :
                        tx_str=tx_str + self.transliterate_ml_en(word)   + " "
                        continue    
                    else:    
                        tx_str = tx_str + " " + word 
                        #tx_str="Not implemented now."
                        #break    
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
        return  "Transliterate the text between any Indian Language"   

def getInstance():
    return Transliterator()     
        
