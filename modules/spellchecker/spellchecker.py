#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,string
import codecs
import re, collections
import codecs
from common import *
from utils import *
class Spellchecker(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'spellchecker.html')
        self.alphabets = None#'abcdefghijklmnopqrstuvwxyz'
        self.NWORDS = None
        self.lang = None
        self.dictionaries = {}
        
    def words(self,text): 
        for punct in string.punctuation:
            text = text.replace(punct,"")
        words = text.split()
        return words
        #return re.findall('[a-z]+', text.lower()) 

    def train(self,features=None):
        if not self.dictionaries.has_key(self.lang) :
            dictionary = os.path.join(os.path.dirname(__file__), 'dicts/'+self.lang+'.dic')
            self.dictionaries[self.lang] = self.words(codecs.open(dictionary,'r',encoding='utf-8', errors='ignore').read())#, errors='ignore'
            print "loaded "  + self.lang +" dictionary"
        return self.dictionaries[self.lang]
    def edits1(self,word):
        """
        Get the words by edit distance 1
        """
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in s for c in self.alphabets if b]
        inserts    = [a + c + b     for a, b in s for c in self.alphabets]
        edits1 =  set(deletes + transposes + replaces + inserts)
        print len(edits1)
        return edits1

    def known_edits2(self,edits1):
        """
        Get the words by edit distance 2
        """
        edits2 = set(e2 for e1 in edits1 for e2 in self.edits1(e1) if e2 in self.NWORDS)
        print len(edits2)
        return edits2

    def known(self,words): 
        """
        Check whether the word is present in the dictionary
        """
        return set(w for w in words if w in self.NWORDS)
    @ServiceMethod
    def suggest(self,word, lang=None):
        word=word.strip()
        if self.lang != lang :
            self.NWORDS = None
        if lang==None :
            self.lang = detect_lang(word)[word]
        else :
            self.lang = lang
        self.alphabets =  charmap[self.lang]
        if self.NWORDS == None:
            self.NWORDS = self.train() 
        if self.check(word):
            return word        
        edits1 =    self.edits1(word)
        candidates = self.known(edits1) or self.known_edits2(edits1) 
        return dumps(list(candidates))
        #return max(candidates, key=self.NWORDS.get)
    
    @ServiceMethod                  
    def check(self, word, lang=None):
        word=word.strip()
        if self.lang != lang :
            self.NWORDS = None
        if lang==None :
            self.lang = detect_lang(word)[word]
        else :
            self.lang = lang
        self.alphabets =  charmap[self.lang]
        if word=="": return True
        if self.NWORDS==None: 
            self.NWORDS = self.train()  
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
