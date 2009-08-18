#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from common import *
from utils import *
from pyuca import Collator 
class Sort(SilpaModule):
	def __init__(self):
		self.template=os.path.join(os.path.dirname(__file__), "sort.html")
		self.collator = Collator(os.path.join(os.path.dirname(__file__), "allkeys.txt"))
		
	@ServiceMethod	
	def sort(self, text):
		words = text.split()
		sorted_words = sorted(words, key=self.collator.sort_key) 
		return dumps(list(sorted_words))

	def get_module_name(self):
		return "Sort"
	def get_info(self):
		return 	"Sorts a set of words linguistically"	

def getInstance():
	return Sort()
		
