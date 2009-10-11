#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import string
import codecs
from common import SilpaModule,ServiceMethod,dumps
from utils import detect_lang
class Spellchecker(SilpaModule):
    
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'spellchecker.html')
        self.NWORDS = None
        self.lang = None
        self.dictionaries = {}
        
    def words(self,text): 
        for punct in string.punctuation:
            text = text.replace(punct,"")
        words = text.split()
        return words

    def train(self,features=None):
        if not self.dictionaries.has_key(self.lang) :
            try:
                dictionary = os.path.join(os.path.dirname(__file__), 'dicts/'+self.lang+'.dic')
                self.dictionaries[self.lang] = self.words(codecs.open(dictionary,'r',encoding='utf-8', errors='ignore').read())#, errors='ignore'
            except:
                self.dictionaries[self.lang] =None  
            #print "loaded "  + self.lang +" dictionary"
        return self.dictionaries[self.lang]
        
    def levenshtein(self,s1, s2):
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
            self.NWORDS = self.train() 
        if self.check(word):
            return word        
        candidates = []
        for candidate in self.NWORDS:
            #Dont check if the first letter is different
            if candidate[0] != word[0]:
                continue
            if len(candidate) - len(word)  > distance or len(word) - len(candidate)  >    distance :
                continue
            if not self.levenshtein(candidate, word) > distance :
                candidates.append(candidate)
        return dumps(candidates)
            
    @ServiceMethod                  
    def check(self, word, language=None):
        word=word.strip()
        if self.lang != language:
            self.NWORDS = None
        if language==None :
            self.lang = detect_lang(word)[word]
        else :
            self.lang = language
        if word=="": return True
        if self.NWORDS==None: 
            self.NWORDS = self.train()  
        if self.NWORDS==None:           
            # Dictionary not found
            return False
        for w in self.NWORDS :
            if word == unicode(w) :
                return True
        return False    

    def get_module_name(self):
        return "Spellchecker"
    def get_info(self):
        return  "Spellchecker module"

def getInstance():
        return Spellchecker()
