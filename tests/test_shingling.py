# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import shingling
#from silpa.modules import ngram
h=shingling.getInstance()
s=h.wshingling("a rose is a rose is a rose")
print s
