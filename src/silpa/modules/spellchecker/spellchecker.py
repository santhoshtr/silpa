# -*- coding: utf-8 -*-
# Spellchecker
# Copyright 2008-2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
import sys
import os
import string
import codecs
from common import SilpaModule,ServiceMethod
from utils import detect_lang, silpautils, silpalogger
from modules.inexactsearch import inexactsearch
from indexer import DictionaryIndex
from common.silparesponse import SilpaResponse
import urllib

class Spellchecker(SilpaModule):
    
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'spellchecker.html')
        self.NWORDS = None
        self.lang = None
        self.dictionaries = {}
        self.response = SilpaResponse(self.template)
        
    def words(self,text): 
        #no need to check for punctuation since we are loading a proof read wordlist
        #for punct in string.punctuation:
        #    text = text.replace(punct,"")
        words = text.split()
        return set(words)

    def train(self,features=None):
        if not self.dictionaries.has_key(self.lang):
            index = DictionaryIndex()
            self.dictionaries[self.lang] = index.load_index(self.lang+".dic")
    
    
    def get_wordlist(self,word=""):
        index = self.dictionaries.get(self.lang,None)
        if index == None:
            self.train()
            index = self.dictionaries.get(self.lang,None)

        words = []
        if word == "":
            return words

        byte_offset = index.get(word[0],None)
        if byte_offset == None:
            return words

        path = os.path.join(os.path.dirname(__file__),"dicts/"+self.lang+".dic")
        fp = codecs.open(path,"r",encoding="utf-8",errors="ignore")
        fp.seek(int(byte_offset))

        while True:
           line = fp.readline().strip()
           if len(line) > 0 and not word[0] == line[0]:
               break
           words.append(line)

        return words

        
    def levenshtein(self,s1, s2):
        """
        Return the levenshtein distance between two string
        """
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
        if not s1:
            return len(s2)
        
        previous_row = xrange(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    
    @ServiceMethod
    def suggest(self,word, language=None, distance=2):
        word=word.strip()
        if word=="": 
            return None
        if self.lang != language:
            self.NWORDS = None
        if language==None :
            self.lang = detect_lang(word)[word]
        else :
            self.lang = language
        if self.NWORDS == None:
            self.NWORDS = self.get_wordlist(word) 
        if word in self.NWORDS:
            return word        
        candidates = []
        for candidate in self.NWORDS:
            #skip if the first letter is different
            #if candidate[0] != word[0]:
            #    continue
            #if the length difference is greater than the threshold distance, skip
            if len(candidate) - len(word)  > distance or len(word) - len(candidate)  >    distance :
                continue
            if not self.levenshtein(candidate, word) > distance :
                candidates.append(candidate)
        candidates = self.filter_candidates(word, candidates)
        if len(candidates)==0:
            #try inserting spaces in between the letters to see if the word got merged
            pos = 2;
            while pos < len(word)-2:
                if self.check(word[:pos],self.lang) and self.check(word[pos:],self.lang):
                    candidates.append(word[:pos]+" "+word[pos:])
                    candidates.append(word[:pos]+"-"+word[pos:])
                pos+=1    
        return candidates
        
    def filter_candidates(self, word, candidates):
        filtered_candidates=[]
        isearch = inexactsearch.getInstance() 
        #TODO sort by score
        for candidate in candidates:
            if isearch.compare(word,candidate) >= 0.6:  #if both words sounds alike - almost
                filtered_candidates.append(candidate)
        return filtered_candidates

            
    @ServiceMethod                  
    def check(self, word, language=None):
        word=word.strip()
        if word == "": 
            return None
        #If it is a number, don't do spelcheck
        if silpautils.is_number(word): 
            return True            
        if self.lang != language:
            self.NWORDS = None
        if language == None :
            self.lang = detect_lang(word)[word]
        else :
            self.lang = language
        if word=="": return True
        
        if self.NWORDS == None: 
            self.NWORDS = self.get_wordlist(word)  
        if self.NWORDS == None:           
            # Dictionary not found
            return False
        result = word in self.NWORDS
        #if it is english word, try converting the first letter to lower case.
        #This will happen if the word is first word of a sentence
        if result == False and word.upper() != word.lower():
            newword = word[0].lower()+word[1:]
            self.NWORDS = self.get_wordlist(newword)  
            return newword in self.NWORDS
        else:
            return result    
            
    def strip_punctuations(self,s):
        """
        Remove all the punctuation characters from the string and return the resulting string
        """
        exclude = set(string.punctuation)
        return  ''.join(ch for ch in s if ch not in exclude)


    @ServiceMethod
    def check_batch(self, text, language=None):
       """
       Return a list of misspelled words give a chunk of text.
       """
       words = urllib.unquote(text)
       words = words.split()
       misspelled_words = []
       for word in words:
           tempword = self.strip_punctuations(word) 
           if not self.check(tempword, language):
               misspelled_words.append(word)
       return misspelled_words

    def get_module_name(self):
        return "Spellchecker"
        
    def get_info(self):
        return "Indic Spellchecker"

def getInstance():
        return Spellchecker()
