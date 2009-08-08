# -*- coding: UTF-8 -*-

import sys
from ddict import *

def submit_line(line):
	odict = open("dict_out", "wb")
        w = line.split()
#	pdb.set_trace()
        for i in range(len(w)):
		if i==0:
			print w[i]
			odict.write(w[i])
		else:
#	                print "word at %d\n", i
        	        print w[i]
			if (i==1):
				odict.write(phoneme[w[i]])
			else:
				if((w[i-1] in cmu_cons)) & (w[i] in cmu_cons):
						odict.write('्')
						odict.write(phoneme[w[i]])
				else:
					if((w[i-1] in cmu_cons) & (w[i]in cmu_vow)):
						odict.write(phoneme_matra[w[i]])
					else:
						odict.write(phoneme[w[i]])

					

#			if phoneme.has_key(w[i]):
#                		odict.write(phoneme[w[i]])
#		        else:
#				odict.write(phoneme_matra[w[i]])
#				print "key not present in ddict"


#def dict_transe(ipstr):
str = "NEW"
fdict = open("cmudict.0.7a_SPHINX_40", "rb")
flines = fdict.readlines()
linecount = len(flines)
i = 44
for l in flines:
	w = l.split()
	if (w[0]==str.upper()):
		i = 1
#		break
print l
#		print "line No.%d", l
#		print w[0]
#		submit_line(l)

#print flines
#print linecount
