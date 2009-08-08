#!/ust/bin/env python
# -*- coding: utf-8 -*-
import random, sys,os

def fortunes(infile,pattern=None):
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

def findfortune(pattern=None):
	filename = os.path.join(os.path.dirname(__file__), 'database/fortune-ml')
	""" Pick a random fortune from a file """
	fortunes_list=fortunes(file(filename),pattern)
	chosen= random.choice(fortunes_list)
	return "".join(chosen)

if __name__ == "__main__":
    print findfortune(),
    print findfortune("enemey<br>"),
    print findfortune(u"ആന"),

