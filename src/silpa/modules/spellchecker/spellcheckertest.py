#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,string
import codecs
import re, collections
import codecs
from  charmap import *
class Spellchecker():
	def __init__(self):
		self.template=os.path.join(os.path.dirname(__file__), 'spellchecker.html')
		self.alphabets = None#'abcdefghijklmnopqrstuvwxyz'
		self.NWORDS=None
		self.lang=None
		
	def words(self,text): 
		for punct in string.punctuation:
			text = text.replace(punct,"")
		words = text.encode('utf-8').split()
		return words
		#return re.findall('[a-z]+', text.lower()) 

	def train(self,features=None):
		if features==None:
			self.dictionary=os.path.join(os.path.dirname(__file__), 'dicts/'+self.lang+'.dic')
			features=self.words(codecs.open(self.dictionary,'r',encoding='utf-8', errors='ignore').read())
		model = collections.defaultdict(lambda: 1)
		for f in features:
			model[f] += 1
		return model

	def edits1(self,word):
		"""
		Get the words by edit distance 1
		"""
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes    = [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in s for c in self.alphabets if b]
		inserts    = [a + c + b     for a, b in s for c in self.alphabets]
		return set(deletes + transposes + replaces + inserts)

	def known_edits2(self,word):
		"""
		Get the words by edit distance 2
		"""
		return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2.encode('utf-8') in self.NWORDS)

	def known(self,words): 
		"""
		Check whether the word is present in the dictionary
		"""
		return set(w for w in words if w in self.NWORDS)
	
	def suggest(self,word, lang=None):
		word=word.strip()
		self.lang=lang
		self.alphabets =  charmap[self.lang]
		if self.NWORDS==None: self.NWORDS = self.train()	
		candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
		return list(candidates)
		#return max(candidates, key=self.NWORDS.get)
	def check(self,word, lang=None):
		word=word.strip()
		if self.lang != lang : 
			self.NWORDS = None
			if lang==None :
				 self.lang = "en_US" #detect lang
			else :
				self.lang = lang
		self.alphabets =  charmap[self.lang]
		if word=="": return True
		if self.NWORDS==None: 
			print "loading the dictionary for " + self.lang
			self.NWORDS = self.train()	
		if word in self.NWORDS:	return True
		return False	
	def get_module_name(self):
		return "Spellchecker"
	def get_info(self):
		return 	"Spellchecker module"
		
if __name__ == '__main__':		
	sp=Spellchecker()
	print sp.check("speling", "en_US")
	print sp.check("spelling", "en_US")
	print sp.suggest("speling", "en_US")
	print sp.check("സന്തഷ്", "ml_IN")
	print sp.suggest(u"സന്തോഷ്", "ml_IN")
