#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tempfile 
from subprocess import Popen
from subprocess import PIPE
class Sort():
	def sort(self,  text_list, lang="en_US"):
		sortedList=[]
		tempInfile = tempfile.NamedTemporaryFile(delete=False)
		tempOutfile = tempfile. NamedTemporaryFile()
		for entry in text_list:
			tempInfile.write(entry.encode("utf-8")+"\n")
		
		cmd="LOCPATH=" + os.path.join(os.path.dirname(__file__), "locales") + " LC_ALL=" + lang +" /usr/bin/sort -u " + 	tempInfile.name  +" -o " +   tempOutfile.name
		print cmd
		os.system(cmd)
		while True:
			sortedWord=tempOutfile.readline()
			print sortedWord
			if sortedWord == "" : 
				break
			sortedList.append(sortedWord)
		'''Closing will delete the temporary file'''	
		tempInfile.close()	
		tempOutfile.close()
		return sortedList
if (__name__ == "__main__"):
	list=[u'സരള',u'റഹ്മാന്‍', u'രമ്യ']
	s=Sort()
	print s.sort(list,"ml_IN")
	print s.sort(list,"en_US")
