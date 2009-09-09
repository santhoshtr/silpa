#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        
