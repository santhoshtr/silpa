# Fortune
# -*- coding: utf-8 -*-
#
#  Copyright © 2009  Santhosh Thottingal <santhosh.thottingal@gmai.com>
#  Released under the GPLV3+ license

import os,random
from common import *
class Fortune(SilpaModule):
	def __init__(self):
		self.template=os.path.join(os.path.dirname(__file__), 'fortune.html')
	
	def fortunes(self,infile,pattern=None):
		""" Yield fortunes as lists of lines """
		result = []
		for line in infile:
			line=line.decode("utf-8")
			if line == "%\n":
				continue
			else:
				if(pattern==None):
					result.append(line)
				else:
					if(line.find(pattern)>0):
						result.append(line)		
		if result:
			return result

	@ServiceMethod			
	def fortune_ml(self, pattern=None):
		filename = os.path.join(os.path.dirname(__file__), 'database/fortune-ml')
		""" Pick a random fortune from a file """
		fortunes_list=self.fortunes(file(filename),pattern)
		chosen=""
		if fortunes_list:
			chosen= random.choice(fortunes_list)
		return "".join(chosen)
	
	def get_module_name(self):
		return "Fortune Malayalam"
	def get_info(self):
		return 	"Get/Search a random Malayalam quote "
def getInstance():
	return Fortune()	
