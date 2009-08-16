#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from common import *
class Sort(SilpaModule):
	def sort(self,  text_list, lang="en_US"):
		sortedList=[]
		os.environ["LOCPATH"]=os.path.join(os.path.dirname(__file__), "locales")
		os.environ["LC_ALL"]=lang
		tempOutfile = tempfile. NamedTemporaryFile()
		tempInfile = open("tempInfile", "w")	
		for entry in text_list:
			tempInfile.write(entry.encode("utf-8")+"\n")
		tempInfile.close()	
		cmd="LOCPATH=" + os.path.join(os.path.dirname(__file__), "locales") + " LC_ALL=" + lang +" /usr/bin/sort -u " + 	tempInfile.name  +" -o " +   tempOutfile.name
		os.system(cmd)
		while True:
			sortedWord=tempOutfile.readline()
			if sortedWord == "" : 
				break
			sortedList.append(sortedWord.decode("utf-8"))
		'''Closing will delete the temporary file'''	
		tempOutfile.close()
		return sortedList
		
	def process(self,form):
		response = """
		<h2>Sort the text</h2></hr>
		<p ><font color="red">This module is buggy. The search results may not be correct. Work in progress..</font>
		</p>
		<p>Enter the words(one word per line) for sorting in the below text area.
		 Language of each  word will be detected. 
		 (Mixed language sorting not supported yet)
		</p>
		<form action="" method="post">
		<textarea  name='input_text' id='id1'>%s</textarea>
		<input  type="submit" id="Sort" value="Sort"  name="action" style="width:12em;"/>
		</br>
		</form>
		"""
		if(form.has_key('input_text')):
			text =form['input_text'].value	.decode('utf-8')
			response=response % text
			words=text.split("\n")
			mm=ModuleManager()
			ld = mm.getModuleInstance("Detect Language")
			lang=ld.detect_lang(words[0])[words[0]]
			sorted_words=self.sort(words,  lang)
			response = response+"<h2>Sorted words("+lang+")</h2></hr>"
			response = response+"<table class=\"table1\"><tr><th>Word</th></tr>"
			for word in sorted_words:
				response = response+"<tr><td>"+word+"</td></tr>"
			response = response+"</table>	"
		else:
			response=response % ""	
		return response	
	def get_module_name(self):
		return "Sort"
	def get_info(self):
		return 	"Sorts a set of words linguistically"	

def getInstance():
	return Sort()
		
if (__name__ == "__main__"):
	list=[u'സരള',u'റഹ്മാന്‍', u'രമ്യ']
	s=Sort()
	s.sort(list,"ml_IN")
	s.sort(list,"en_US")
